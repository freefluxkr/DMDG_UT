
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

import numpy as np
import pandas as pd

# =======================================
# 0. 데이터 불러오기
# =======================================

url = "https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv"

df = pd.read_csv(url,sep='\t')

print('[결측치]',"\n",df.isnull().sum())

# ========================================
# 1. Name 열 -> 호칭 5개로 구분해서 숫자로
# ========================================
def get_title(name):
    # Braund, Mr. Owen Harris
    # name.split(', ')
    # , : Braund | Mr. Owen Harris
    # ["Braund", "Mr. Owen Harris"] -> name.split(', ')[1]
    # name.split(', ')[1] => Mr. Owen Harris
    # . : ["Mr"," Owen Harris"][0]
    title = name.split(', ')[1].split('. ')[0]
    if title == 'Mr':
        return 0
    elif title == 'Miss':
        return 1
    elif title == 'Mrs':
        return 2
    elif title == 'Master':
        return 3
    else:
        return 4
# 'Name'컬럼에 있는 값들에다가 get_title 함수를 적용 시키겠다.
# 그 후에 'Title' 컬럼(열)을 새로만들어서 그 열의 값들로 저장하겠다.
df['Title'] = df['Name'].apply(get_title)
print("="*60,"\n",df['Title'].map({0: 'Mr', 1: 'Miss', 2: 'Mrs', 3: 'Master', 4: 'Etc'}).value_counts())

# ========================================
# 2. Age 빈 값(결측치) -> 호칭별 중앙값으로 채우기
# ========================================
# t==0=='Mr'<'Title'
for t in [0,1,2,3,4]:
    # 호칭이 t인 사람들만 골라서 나이의 중앙값 계산
    # .median() : 값들을 크기 순으로 줄 세웠을 때 정중앙에 있는 값
    median_age = df[df['Title']==t]['Age'].median()

    # 호칭이 t면서 Age가 비어있는 행의 Age 칸에만 중앙값을 넣음
    df.loc[(df['Title']==t) & (df['Age'].isnull()), 'Age'] = median_age

print("="*60,"\n","중앙값 채운 후 Age 빈 값 : ",df['Age'].isnull().sum())

# ========================================
# 3. Sex 숫자로
# ========================================
# .map(dictionary) : 열의 각 값을 딕셔너리에서 찾아 바꿔줌
# 'male' 0, 'famale' 1
df['Sex'] = df['Sex'].map({'male':0,'female':1})

# ========================================
# 4. Embarked 열 (빈 값 2개는 drop, 나머지는 숫자로)
# ========================================
# dropna : 빈 값이 있는 행을 지움
# subset=['Embarked'] : Embarked 열이 비어있는 행만 골라서 삭제 (다른 열은 안 봄)
df = df.dropna(subset=['Embarked'])
# 'S'(사우샘프턴)→0, 'C'(셰르부르)→1, 'Q'(퀸스타운)→2
df['Embarked'] = df['Embarked'].map({'S':0,'C':1,'Q':2})

# ========================================
# 5. Sibsp, Parch -> 가족 수 열로 합치기
# ========================================
# Sibsp(형제/배우자 수) + Parch(부모/자녀 수) + 1(본인) = 함께 탄 가족 인원
df['Family'] = df['SibSp'] + df['Parch'] + 1

# ========================================
# 6. Fare -> 개인별 요금 Fare_person 열 추가
# ========================================
# Fare : 가족이 함께 끊은 표 값을 1인당 요금으로 나누기
df['Fare_person'] = df['Fare'] / df['Family']

# ========================================
# 7. 최종 데이터 확인
# ========================================
# 학습에 사용되는 데이터 독립변수(X), 종속변수(y)로 나누기
features = ['Pclass', 'Sex', 'Age', 'Embarked', 'Family', 'Fare_person', 'Title']
X = df[features]
y = df['Survived']

print("="*60,"\n",X.head())
print("="*60,"\n","[결측치] \n",X.isnull().sum())

# ========================================
# 모델 비교
# ========================================
# 전체 데이터를 학습용 : 시험용 = 8 : 2로 나누기
# random_state = 42
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=42)

# 모델 분류
models = {
    '결정트리': DecisionTreeClassifier(random_state=42),
    '랜덤포레스트': RandomForestClassifier(random_state=42),
    '로지스틱회귀': LogisticRegression(max_iter=1000),
    '나이브베이즈': GaussianNB(),
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(),
}

best_name = ''
best_score = 0
print("="*60)
# dictionary.item() -> name = '결정트리', model = DecisionTreeClassifier(...)
for name, model in models.items():
    model.fit(X_train,y_train)
    score = model.score(X_test,y_test)
    print(name, ':', round(score,4))

    if score > best_score:
        best_score = score
        best_name = name

print("="*60,"\n",'가장 정확도가 높은 모델 : ',best_name, round(best_score,4))

# ========================================
# 랜덤 포레스트 교차 검증
# ========================================
from sklearn.model_selection import cross_val_score
rf = RandomForestClassifier(random_state=42)

# cv(cross_value : 교차검증 횟수)
scores = cross_val_score(rf,X,y,cv=5)

print("="*60,"\n",'5번의 정확도 : ', scores)
print("\n",'평균 정확도 : ',scores.mean())

# ========================================
# 승객 생존율 예측
# ========================================
import matplotlib as plt
# ========================================
# 랜덤포레스트 생존 예측 + 시각화
# ========================================
import matplotlib.pyplot as plt

# 맥에서 그래프에 한글을 쓰려면 한글 폰트를 지정해야 함 (안 하면 □□□ 로 깨짐)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False   # 한글 폰트 사용 시 마이너스(-) 기호 깨짐 방지

# 랜덤포레스트를 학습시키고, 시험 데이터의 생존 여부를 예측
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)   # X_test 한 행(승객 1명)마다 0(사망)/1(생존) 예측값이 담긴 배열

# subplots(2, 2) : 2행 2열, 그래프 4칸짜리 도화지를 만듦
# fig = 도화지 전체, axes = 칸 4개 (axes[0,0]=왼쪽 위, axes[0,1]=오른쪽 위,
#                                   axes[1,0]=왼쪽 아래, axes[1,1]=오른쪽 아래)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# ----- 실제 vs 예측 생존자 수 -----
# y_test == 1 → 실제 생존자만 True인 Series → .sum()으로 True 개수를 셈 (isnull().sum()과 같은 원리)
actual = [(y_test == 0).sum(), (y_test == 1).sum()]   # [실제 사망자 수, 실제 생존자 수]
pred   = [(y_pred == 0).sum(), (y_pred == 1).sum()]   # [예측 사망자 수, 예측 생존자 수]

x = np.arange(2)   
# 막대를 세울 가로 위치 [0, 1] (0=사망 자리, 1=생존 자리)
# 같은 자리에서 실제 막대는 왼쪽으로 0.2, 예측 막대는 오른쪽으로 0.2 비켜 세워 나란히 비교
axes[0, 0].bar(x - 0.2, actual, width=0.4, label='실제', color='#4269d0')
axes[0, 0].bar(x + 0.2, pred,   width=0.4, label='예측', color='#c65911')
axes[0, 0].set_xticks(x)                             
axes[0, 0].set_xticklabels(['사망(0)', '생존(1)'])    
axes[0, 0].set_ylabel('명')
axes[0, 0].set_title('시험 데이터: 실제 vs 예측')
axes[0, 0].legend()   

# ----- 성별 생존율 -----
# Survived가 0/1이라서 평균(.mean())을 내면 곧 생존율이 됨
rate_sex = df.groupby('Sex')['Survived'].mean()  
axes[0, 1].bar(['남자(0)', '여자(1)'], rate_sex, color='#4269d0')
axes[0, 1].set_ylabel('생존율')
axes[0, 1].set_title('성별 생존율')

# ----- 객실 등급별 생존율 -----
rate_pclass = df.groupby('Pclass')['Survived'].mean()   # 인덱스 1,2,3등석별 생존율
axes[1, 0].bar(['1등석', '2등석', '3등석'], rate_pclass, color='#4269d0')
axes[1, 0].set_ylabel('생존율')
axes[1, 0].set_title('객실 등급별 생존율')

plt.show()         
