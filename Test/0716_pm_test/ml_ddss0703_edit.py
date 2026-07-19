import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


# 파일 읽기
url = "https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv"
df= pd.read_csv(url, sep="\t")

print(df.head())
print(df.columns)
# print(df['Embarked'].unique()) #['S', 'C', 'Q', nan]

# 2. 데이터 전처리
'''
- 여성과 아이가 먼저 구조되었는지
- 가족이 함께 탄 사람들이 더 많이 생존했는지
- 비용과 티켓 등급에 따라 생존율이 높은지
Index(['PassengerId\tSurvived\tPclass\tName\tSex\tAge\tSibSp\tParch\tTicket\tFare\tCabin\tEmbarked'], dtype='str')
Index(['승객 일련번호\t생존 여부\t티켓 등급\t이름\t성별\t나이\t동반한 형제자매/배우자 수\t동반한 부모/자녀 수\t티켓 번호\t운임(요금)\t객실 번호\t탑승 항구']
'''

# ① 승객 생존율을 예측하기 위한 컬럼 골라내기
# Survived:생존여부, Sex:성별, Age:나이, SibSp:동반한 형제자매/배우자, Parch:동반한 부모/자녀 수, Fare:운임(요금)
essential_cols = ['Survived', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Pclass']
df_pass = df[essential_cols].copy()

# ② 결측치 확인하기
# print(df_pass.info())
# print(df_pass.isnull().sum())

# ②-1 나이(Age) 열에 결측치 30개, 승객들의 '평균 나이'로 채우기
mean_age = df_pass['Age'].mean()
df_pass['Age'] = df_pass['Age'].fillna(mean_age)

# ②-2 컴퓨터가 이해할 수 있게 글자를 숫자로 바꾸기(맵핑)
df_pass['Sex'] = df_pass['Sex'].map({'female': 0, 'male': 1})

# print("✓ 전처리가 완료되었습니다.")
print("="*50 + "\n")

# ==========================================
# 3. 데이터 분리
# 지정한 컬럼들 = 독립변수(문제지X), Survived = 종속변수(정답지y)
X=df_pass.drop(columns=['Survived'])
y=df_pass['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#print(f"학습용 문제집 개수: {len(X_train)}개") #124
#print(f"시험용 문제집 개수: {len(X_test)}개") #32

# 의사결정나무 : 스무고개 모델(질문이 많아지면 규칙을 억지로 외워버리는 오류 발생)
model_tree = DecisionTreeClassifier(max_depth=5, random_state=42)
model_tree.fit(X_train, y_train) # 학습
predictions = model_tree.predict(X_test) # 예측
# 실제 정답(y_test)과 모델이 예측한 답(predictions)을 비교해서 정확도를 계산
score = accuracy_score(y_test, predictions)
print(f"의사결정나무 모델의 예측 정확도: {score * 100:.2f}%") # 75.00%

# 랜덤 포레스트 : 다수결, 오답률이 확 떨어진다.(시간이 오래걸림)
model_rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model_rf.fit(X_train, y_train)
predictions = model_rf.predict(X_test)
score = accuracy_score(y_test, predictions)
print(f"랜덤 포레스트 모델의 예측 정확도: {score * 100:.2f}%") # 71.88%

# 로지스틱 회귀분석 : 계산 과정 단순(특정 나이대, 특정 성별이 많은수록 오류 발생 가능성 높다)
model_lr = LogisticRegression(C=1.0, l1_ratio=0, solver='lbfgs', random_state=42)
model_lr.fit(X_train, y_train)
predictions = model_lr.predict(X_test)
score = accuracy_score(y_test, predictions)
print(f"로지스틱 회귀분석의 예측 정확도: {score * 100:.2f}%") # 71.88%

# SVM 모델 : 두 그룹으로 선으로 나누는 것 > 양쪽 그룹과 최대한 멀리 떨어진 공간(여백)을 확보하며 선을 긋는다.
model_svm = LinearSVC(C=1.0, random_state=42)
model_svm.fit(X_train, y_train)
predictions = model_svm.predict(X_test)
score = accuracy_score(y_test, predictions)
print(f"SVM 모델의 예측 정확도: {score * 100:.2f}%") # 68.75%

# 처음 컬럼 (Survived:생존여부, Sex:성별, Age:나이, SibSp:동반한 형제자매/배우자, Parch:동반한 부모/자녀 수)으로
# 생존율을 예측했을 때 보다 Fare:운임(요금)을 추가하였을 때 생존율이 더 높게 나왔다.
# => 승객의 경제적인 능력이 클수록 생존율에 영향을 미쳤다.(등급이나 운임 요금이 높을수록 좋은 위치의 자리가 배치되기 때문)




























# 실제로 등급이 생존율에 영향을 미치는지 그룹핑해서 알아보기
print(df.groupby('Pclass')['Survived'].mean())

# 운임요금이 생존율에 영향을 미치는지 그룹핑해서 알아보기
def charge(fee):
    if fee < 10:
        return '저가 (10달러 미만)'
    elif fee < 30:
        return '중가 (10~30달러)'
    else:
        return '고가 (50달러 이상)'
df['fare'] = df['Fare'].apply(charge)
fare = df.groupby('fare')['Survived'].mean()
print(fare)













