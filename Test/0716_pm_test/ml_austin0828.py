'''
칼럼 의미
PassengerId승 객 고유 번호 (단순 일련번호, 분석에 큰 의미 없음)
Survived생존 여부 — 0: 사망, 1: 생존 (이게 바로 예측하려는 **정답(y)**이에요)
Pclass 객실 등급 — 1등석, 2등석, 3등석 (숫자가 작을수록 고급 객실)
Name 승객 이름
Sex 성별 (male/female)
Age 나이
SibSp 함께 탑승한 형제자매(Sibling)/배우자(Spouse)의 수
Parch 함께 탑승한 부모(Parent)/자녀(Child)의 수
Ticket 티켓 번호
Fare 운임(요금)
Cabin 객실 번호 (결측치가 굉장히 많은 컬럼으로 유명해요)
Embarked 탑승한 항구 — C(Cherbourg), Q(Queenstown), S(Southampton)
'''
import pandas as pd
from sklearn.model_selection import train_test_split
#과거의 데이터 준비
path = "https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv"
passenger = pd.read_csv(path,sep='\t')
passenger['Title'] = passenger['Name'].str.extract(r',\s*([^\.]*)\.')

def classify_title(title):
    if title in ['Mr', 'Mrs', 'Miss', 'Master']:
        return title
    else:
        return 'Rare'

passenger['Title'] = passenger['Title'].apply(classify_title)
passenger['FamilySize'] = passenger['SibSp'] + passenger['Parch'] + 1
passenger['FarePerPerson']=passenger['Fare']/passenger['FamilySize']
print(passenger)
#독립변수와 종속변수 분리
independent=passenger[['Title', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
dependent = passenger[["Survived"]]


print(independent['Age'].isnull().sum())# 결측치 계산
independent['Age']=independent['Age'].fillna(independent['Age'].mean())# 결측치 처리
print(independent['Age'].isnull().sum())# 결측치처리 됐는지
independent['Embarked']=independent['Embarked'].fillna('S')# 결측치 처리
print(independent['Embarked'].isnull().sum())# 결측치처리 됐는지

print(independent['SibSp'])
print(independent['Parch'])
print(independent['Embarked'])
X_train, X_test, y_train, y_test = train_test_split(independent, dependent, test_size=0.2, random_state=42)

# 문자열 컬럼만 원-핫 인코딩
X_train = pd.get_dummies(
    X_train,
    columns=['Title', 'Sex', 'Embarked'],
    drop_first=True      # 다중공선성 방지를 위해 첫 번째 열 제거(선택사항)
)

X_test = pd.get_dummies(
    X_test,
    columns=['Title', 'Sex', 'Embarked'],
    drop_first=True
)
print(X_train.columns)
print(X_test.columns)

print(X_train.isnull().sum())
print(X_train.dtypes)


import time
# 모델의 학습 진행율을 보기 위한 라이브러리
from tqdm import tqdm
###1 결정 트리(Decision Tree)
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
#결정 트리 모델 생성 및 학습

dt_model = DecisionTreeClassifier(random_state=42)
print("모델 학습을 시작합니다...")
# 기존의 range(100) 대신 tqdm(range(100))을 사용.
for epoch in tqdm(range(100), desc="[Epoch 학습 중]"):
    dt_model.fit(X_train, y_train)
print("학습이 완료되었습니다!")
# 테스트 데이터로 예측 및 정확도 확인
dt_pred = dt_model.predict(X_test)
print(f"결정 트리 정확도 : {accuracy_score(y_test, dt_pred):.2f}")


### 2 랜덤 포레스트
from sklearn.ensemble import RandomForestClassifier

# 랜덤 포레스트 모델 생성 ( 나무를 100개 만들도록 설정) 및 학습
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)#n_estimators: 의사 결정 트리를 몇개 만들건지
dt_model = DecisionTreeClassifier(random_state=42)
print("모델 학습을 시작합니다...")
for epoch in tqdm(range(100),desc="[Epoch 학습 중"):
    rf_model.fit(X_train, y_train)
    #time.sleep(0.05)
print("모델 학습이 종료되었습니다...")
#예측 및 정확도 확인
rf_pred = rf_model.predict(X_test)
print(f"랜덤 포레스트 정확도 : {accuracy_score(y_test, rf_pred):.2f}")
### 3. k-최근접 이웃( KNN: k-nearest neighbors)
from sklearn.neighbors import KNeighborsClassifier

# KNN 모델 생성 ( 가장 가까운 이웃 3개를 참고하도록 설정) 및 학습
knn_model = KNeighborsClassifier(n_neighbors=3)
print("모델 학습을 시작합니다...")
for epoch in tqdm(range(100),desc="[Epoch 학습 중"):
    knn_model.fit(X_train, y_train)
    #time.sleep(0.05)
print("모델 학습이 종료되었습니다...")
# 예측 및 정확도 확인
knn_pred = knn_model.predict(X_test)
print(f"KNN 정확도: {accuracy_score(y_test,knn_pred):.2f}")

###4. 서포트 벡터 머신(SVM: support vector machine)
from sklearn.svm import SVC

#SVM 모델 생성 (분류 기준을 직선으로 설정) 및 학습
svm_model = SVC(kernel='linear',random_state=42)
print("모델 학습을 시작합니다.")
for epoch in tqdm(range(100),desc="[Epoch 학습 중]"):
    svm_model.fit(X_train, y_train)
    #time.sleep(0.05)
print("모델 학습이 종료되었습니다....")

# 예측 및 정확도 확인
svm_pred = svm_model.predict(X_test)
print(f"SVM 정확도: {accuracy_score(y_test,svm_pred):.2f}")

###5. 인공 신경망 (Artificial Neural Networks)
from sklearn.neural_network import MLPClassifier

#인공 신경망 모델 생성 (최대 1000번 반복 학습하도록 설정) 및 학습
ann_model= MLPClassifier(max_iter=1000,random_state=42)
print("모델 학습을 시작합니다...")
for epoch in tqdm(range(100),desc="[Epoch 학습 중]"):
    ann_model.fit(X_train, y_train)
    #time.sleep(0.05)
print("모델 학습이 종료되었습니다....")
#예측 및 정확도 확인
ann_pred = ann_model.predict(X_test)
print(f"인공 신경망 정확도: {accuracy_score(y_test,ann_pred):.2f}")