import ssl
ssl._create_default_https_context = ssl._create_unverified_context
'''
1. 승객 생존율 예측
2. 첨부 데이터를 이용하여 다양한 머신러닝 모델 적용 및 머신러닝 기법에 적용하여
각 ML 모델의 특성과 사용방법 정리 및 요약
'''

import pandas as pd
from pandas import DataFrame as df

# 1. 파일 읽어오기
path = 'https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv'
titanic = pd.read_csv(path,sep='\t')
titanic.head()

print(titanic.info())
'''
## 결측치 존재
<class 'pandas.DataFrame'>
RangeIndex: 156 entries, 0 to 155
Data columns (total 12 columns):
 #   Column       Non-Null Count  Dtype  
---  ------       --------------  -----  
 0   PassengerId  156 non-null    int64  
 1   Survived     156 non-null    int64  
 2   Pclass       156 non-null    int64  
 3   Name         156 non-null    str    
 4   Sex          156 non-null    str    
 5   Age          126 non-null    float64
 6   SibSp        156 non-null    int64  
 7   Parch        156 non-null    int64  
 8   Ticket       156 non-null    str    
 9   Fare         156 non-null    float64
 10  Cabin        31 non-null     str    
 11  Embarked     155 non-null    str    
dtypes: float64(2), int64(5), str(5)
memory usage: 21.0 KB
None
'''
df.isnull(titanic).sum()
'''
PassengerId      0
Survived         0
Pclass           0
Name             0
Sex              0
Age             30
SibSp            0
Parch            0
Ticket           0
Fare             0
Cabin          125
Embarked         1
dtype: int64
'''
##################
## 데이터 전처리
###################

### 결측치

# Cabin : 삭제
titanic = titanic.drop("Cabin", axis=1)
# Embarked : 최빈값으로 대체
titanic["Embarked"] = titanic["Embarked"].fillna(titanic["Embarked"].mode()[0])
# Age는 아래에서 다른거 구해서 처리 예정

df.isnull(titanic).sum()
'''
# 결측치 보정 완료

PassengerId     0
Survived        0
Pclass          0
Name            0
Sex             0
Age            30
SibSp           0
Parch           0
Ticket          0
Fare            0
Embarked        0
dtype: int64
'''

# 가족 규모(family size)
titanic["Family Size"] = titanic["SibSp"]+titanic["Parch"]

# 인당 티켓값
# Fare : 총 납부금액
titanic["Fare Person"] = titanic["Fare"]/(titanic["Family Size"]+1)

# 각 수치 숫자화
titanic["Sex"] = titanic["Sex"].map({"male":1,"female":0})
titanic["Embarked"] = titanic["Embarked"].map({"S":0,"C":1,"Q":2})

# 호칭을 통한 인물 계층화
titanic["Identity"] = titanic["Name"].str.extract(r' ([A-Za-z]+)\.', expand=False)

# 적은 인물 합침
titanic["Identity"] = titanic["Identity"].replace(['Rev', 'Don'], 'Other')

titanic["Identity"].value_counts()
'''
Identity
Mr        89
Miss      34
Mrs       22
Master     8
Other      3
Name: count, dtype: int64
'''

titanic["Identity"] = titanic["Identity"].map({'Mr':0, 'Mrs':1, 'Miss':2, 'Master':3, 'Other':4})
titanic["Identity"].value_counts()

## 필요없는 열 삭제
titanic = titanic.drop("Ticket", axis=1)
titanic = titanic.drop("Name", axis=1)

# 결측치 Age : 호칭별 중앙값으로 처리
def fillna_age_mean(titanic):
    age_mean=titanic.groupby("Identity")["Age"].median()
        #Identity
        #Don       40.0
        #Master     4.0
        #Miss      17.5
        #Mr        28.0
        #Mrs       31.0
        #Rev       46.5
        #Name: Age, dtype: float64

    for i in titanic[titanic["Age"].isnull()].index:
        d=titanic.loc[i,"Identity"]
        titanic.loc[i,"Age"]=age_mean[d]

    return titanic

titanic = fillna_age_mean(titanic)

titanic["Age"].isnull().sum()
'''
np.int64(0)
'''

#-----------------------------------------------------------------------
'''
결정트리
랜덤포레스트
k 이웃 모델
svm 모델

로지스틱 회귀분석
나이브 베이지안 모델
퍼셉트론 모델
확률적 경사하강법 모델
'''
#######################
# 승객 생존율 예측
#######################

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time
from tqdm import tqdm


# 데이터 준비

df.isnull(titanic).sum()
'''
PassengerId    0
Survived       0
Pclass         0
Sex            0
Age            0
SibSp          0
Parch          0
Fare           0
Embarked       0
Family Size    0
Fare Person    0
Identity       0
dtype: int64
'''

X = titanic[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Family Size','Fare Person','Identity']]
y = titanic['Survived']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

#####
## 1. 결정 트리
'''
- 질문을 하나씩 하면서 데이터를 분류하는 알고리즘. 계속하면서 답을 찾는 방식
- 나무 형태로 의사결정 수행
- 장점: 이해하기 쉬움. 결과를 사람이 해석하기 쉬움
- 단점: 데이터에 너무 맞춰(과적합) 학습되기 쉬움. 데이터가 조금만 바뀌어도 트리 구조가 크게 변함
'''

from sklearn.tree import DecisionTreeClassifier

dt_model = DecisionTreeClassifier(random_state=42)
print("모델 학습 시작")

for epoch in tqdm(range(100), desc="[Epoch 학습중]"):
    dt_model.fit(X_train,y_train)
    time.sleep(0.05)
print("학습 완료!")

# 예측 및 정확도 확인
dt_pred = dt_model.predict(X_test)
print(f'결정 트리 정확도: {accuracy_score(y_test,dt_pred):.2f}')
'''
결정 트리 정확도: 0.72
'''


#####
## 2. 랜덤 포레스트
'''
- 여러 개의 결정트리를 만들어 각각 예측한 후, 다수결 또는 평균을 이용하여 최종결과를 결정
- 한 사람의 의견이 아닌, 여러 전문가의 의견을 종합하여 결정하는 방식
- 장점: 결정트리보다 정확하고 안정적. 과적합이 적음. 가장 많이 사용되는 머신러닝 알고리즘 중 하나
'''
from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)
print("모델 학습을 시작합니다 ...")
for epoch in tqdm(range(100), desc='[Eposh 학습 중]'):
    rf_model.fit(X_train, y_train)
    time.sleep(0.05)
print('모델 학습 종료!')

# 예측 및 정확도 확인
rf_pred = rf_model.predict(X_test)
print(f'랜덤 포레스트 정확도: {accuracy_score(y_test, rf_pred):.2f}')

'''
랜덤 포레스트 정확도: 0.78
'''



#####
## 3. k-최근접 이웃
'''
- 새로운 데이터가 주어졌을 때, 주변에 가장 가까운 K개의 데이터를 참고하여 예측
- 가장 많이 속해 있는 그룹으로 새로운 데이터를 분류하는 단순하고 직관적인 방법
- "끼리끼리 모인다"는 원리
- 장점: 원리가 매우 쉬움. 별도의 학습과정 거의 없음
- 단점: 데이터가 많아질수록 속도가 느려짐. K값 선택이 중요함
'''

from sklearn.neighbors import KNeighborsClassifier

k_model = KNeighborsClassifier(n_neighbors=3)
print("모델 학습중~")

for epoch in tqdm(range(100), desc="Eposh 공부중.."):
    k_model.fit(X_train,y_train)
    time.sleep(0.05)
print("KNN 모델 학습 종료!")

# 예측 및 정확도 확인
k_pred = k_model.predict(X_test)
print(f'KNN 정확도: {accuracy_score(y_test,k_pred):.2f}')
'''
KNN 정확도: 0.62
'''



#####
## 4. 서포트 벡터 머신
'''
- 서로 다른 두 그룹을 가장 넓은 간격(Margin)으로 구분하는 경계선을 찾는 알고리즘
- 분류 문제에서 많이 사용
- 두 집단 사이에 가장 안전한 도로 하나를 긋는 방식. 새로운 데이터가 들어왔을 때 어느 쪽에 속하는지 명확하게 판단할 수 있음
- 장점: 분류 성능이 우수함. 적은 데이터에서도 좋은 성능을 내는 경우가 있음
'''

from sklearn.svm import SVC

svm_model = SVC(kernel='linear', random_state=42)
print('모델학습시작')

for epoch in tqdm(range(100), desc="Eposh 공부중.."):
    svm_model.fit(X_train, y_train)
    time.sleep(0.05)
print("모델 학습 종료!")

# 예측 및 정확도 확인
svm_pred = svm_model.predict(X_test)
print(f'SVM 정확도: {accuracy_score(y_test,svm_pred):.2f}')
'''
SVM 정확도: 0.69
'''



#####
## 5. 로지스틱 회귀분석 (Logistic Regression)
'''
- 각 변수(성별, 나이 등)에 가중치를 곱하고 더해서, 생존할 확률이 얼마인지 계산하는 방식
- 이름은 "회귀"지만 실제로는 분류에 사용됨. "몇 % 확률로 생존인가"를 직선 대신 S자 곡선으로 판단하는 방식
- 장점: 계산이 빠르고 결과 해석이 쉬움. 어떤 변수가 생존에 얼마나 영향을 주는지 숫자로 확인 가능
- 단점: 데이터가 복잡하고 비선형적인 패턴일 경우 성능이 떨어질 수 있음
'''
from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression(random_state=42)
print('모델학습시작')

for epoch in tqdm(range(100), desc="Eposh 공부중.."):
    lr_model.fit(X_train, y_train)
    time.sleep(0.05)
print("모델 학습 종료!")

# 예측 및 정확도 확인
lr_pred = lr_model.predict(X_test)
print(f'회귀분석 정확도: {accuracy_score(y_test,lr_pred):.2f}')
'''
회귀분석 정확도: 0.75
'''




#####
## 6. 나이브 베이지안 (Naive Bayes)
'''
- 확률(베이즈 정리)을 이용해서 "이 사람이 생존할 확률 vs 사망할 확률" 중 더 높은 쪽으로 예측
- 변수들이 서로 관련 없다고 "순진하게(naive)" 가정하고 계산 — 실제로는 완전히 독립적이지 않아도 꽤 잘 작동하는 경우가 많음
- 장점: 계산이 매우 빠름. 데이터가 적어도 잘 작동함
- 단점: 변수들끼리 실제로 연관 있는 경우(예: 등급과 요금) 정확도가 떨어질 수 있음
'''
from sklearn.naive_bayes import GaussianNB

nb_model = GaussianNB()
print('모델학습시작')

for epoch in tqdm(range(100), desc="Eposh 공부중.."):
    nb_model.fit(X_train, y_train)
    time.sleep(0.05)
print("모델 학습 종료!")

# 예측 및 정확도 확인
nb_pred = nb_model.predict(X_test)
print(f'나이브 정확도: {accuracy_score(y_test,nb_pred):.2f}')
'''
나이브 정확도: 0.72
'''

#####
## 7. 퍼셉트론 (Perceptron)
'''
- 인공신경망의 가장 기본 단위(뉴런 1개)를 흉내낸 모델. 입력값에 가중치를 곱하고 더한 뒤, 기준선을 넘으면 생존/못 넘으면 사망으로 딱 잘라 판단
- 직선 하나로 두 그룹을 나누려고 시도하는 가장 단순한 신경망 구조
- 장점: 딥러닝의 기본 원리를 보여주는 가장 단순한 모델
- 단점: 복잡한 패턴은 잘 못 잡음. 다른 모델보다 정확도 낮게 나오는 경우가 많음
'''
from sklearn.linear_model import Perceptron

pt_model = Perceptron(max_iter=1000, eta0=1.0, random_state=42)
print('모델학습시작')

for epoch in tqdm(range(100), desc="Eposh 공부중.."):
    pt_model.fit(X_train, y_train)
    time.sleep(0.05)
print("모델 학습 종료!")

# 예측 및 정확도 확인
pt_pred = pt_model.predict(X_test)
print(f'퍼셉트론 정확도: {accuracy_score(y_test,pt_pred):.2f}')
'''
퍼셉트론 정확도: 0.72
'''

#####
## 8. 확률적 경사하강법 (Stochastic Gradient Descent, SGD)
'''
- 정확히는 독립적인 '모델'이라기보다, 모델을 학습시키는 '방법'에 가까움. 데이터를 조금씩 나눠보면서 오차를 줄이는 방향으로 빠르게 값을 조정해가는 방식
- sklearn에서는 기본적으로 로지스틱 회귀와 비슷한 계산을 SGD 방식으로 수행
- 장점: 데이터가 매우 많을 때 학습 속도가 빠름
- 단점: 데이터가 적으면(지금처럼 156명 정도) 장점이 크게 드러나지 않음로지스틱 회귀분석
'''

from sklearn.linear_model import SGDClassifier

sg_model = SGDClassifier(loss='log_loss', penalty='l2', random_state=42)
print('모델학습시작')

for epoch in tqdm(range(100), desc="Eposh 공부중.."):
    sg_model.fit(X_train, y_train)
    time.sleep(0.05)
print("모델 학습 종료!")

# 예측 및 정확도 확인
sg_pred = sg_model.predict(X_test)
print(f'경사하강 정확도: {accuracy_score(y_test,sg_pred):.2f}')
'''
경사하강 정확도: 0.38
'''

##------------------------------------------------------------------------

#### 정확도 비교
'''
결정 트리 정확도: 0.72
랜덤 포레스트 정확도: 0.78
KNN 정확도: 0.62
SVM 정확도: 0.69
회귀분석 정확도: 0.75
나이브 정확도: 0.72
퍼셉트론 정확도: 0.72
경사하강 정확도: 0.38
'''

### 가장 정확한 건 랜덤 포레스트
# 왜?
'''
결정트리의 단점을 구조적으로 보완했기 때문
랜덤 포레스트는 여러개의 트리를 조금씩 다르게 무작위로 뽑아 만들고, 그것으로 학습함
이후 최종 결과를 다수결(투표)로 결정함
타이타닉 데이터는 작은 편이라 이상치의 영향을 받기 쉽지만 
랜덤포레스트는 이상치를 평균내서 잡아주고 과적합도 상쇄되어 훨씬 좋은 성능이 나오는 것
'''


### 랜덤 포레스트 교차검증

from sklearn.model_selection import cross_val_score

rf_model = RandomForestClassifier(random_state=42)

# cv=5 → 5-fold 교차검증 (5조각으로 나눠서 5번 검증)
scores = cross_val_score(rf_model, X, y, cv=5)

print("5번 검증 결과:", scores)
print(f"평균 정확도: {scores.mean():.2f}")
print(f"표준편차: {scores.std():.2f}")

'''
5번 검증 결과: [0.78125    0.80645161 0.83870968 0.74193548 0.67741935]
평균 정확도: 0.77
표준편차: 0.06
'''