import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import tensorflow as tf
import pandas as pd
import numpy as np

url = 'https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv'
df = pd.read_csv(url, sep='\t')
'''
print('행, 열:', df.shape)
print(df.head(5))
print(df.info())
print(df.isnull().sum())
'''

# 최종 데이터 확인 --------------------------------------------------

data=df[['Survived','Pclass','Name','Sex','Age','SibSp','Parch','Fare','Embarked']]

## 1. Name열을 5개로 구분하고 숫자형 데이터로 바꾸기

data['Title']=data['Name'].str.split(',').str[1].str.split('.').str[0]
#print(data['Title'].value_counts())
data['Title'] = data['Title'].str.strip()
data['Title']=data['Title'].replace({'Rev':'Rare','Don':'Rare'})

data['Title']=data['Title'].replace({'Mr':0,'Miss':1,'Mrs':2,'Master':3,'Rare':4})


## 2. age열의 빈 값을 호칭별 중앙값으로 바꾸기
data['Age'] = data['Age'].fillna(data.groupby('Title')['Age'].transform('median'))

## 3. sex 열에서 'male':0,'female':1 로 바꾸기
data['Sex']=data['Sex'].replace({'male':0,'female':1})

## 4. embarked 열
data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])
data['Embarked']=data['Embarked'].replace({'S':0,'C':1,'Q':2})

## 5. sibsp, parch 열
data['Family'] = data['SibSp']+data['Parch']+1

## 6. fare열, 개인별 요금 나타내는 fare_perso열 추가
data['Fare_perso'] = data['Fare']/data['Family']

## 7. 최종 데이터
data
'''
print(data.head())
print(data.shape)
print(data.isnull().sum())
'''

#===================================================================
# 2. 필요한 라이브러리 불러오기

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

#독립변수
X=data[['Pclass','Title','Sex','Age','Family','Fare','Embarked']]
#종속변수
y=data['Survived']

train_X, test_X, train_y, test_y = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

scaler = StandardScaler()
train_X = scaler.fit_transform(train_X)
test_X = scaler.transform(test_X)

#===================================================================
# 2. 모델 학습

import time
from tqdm import tqdm

dt = DecisionTreeClassifier(random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
lr = LogisticRegression(max_iter=1000, random_state=42)
gnb = GaussianNB()
knn = KNeighborsClassifier(n_neighbors=5)
svc = SVC(kernel='linear',random_state=42)
per = Perceptron(max_iter=1000,random_state=42)
sgd = SGDClassifier(max_iter=1000,random_state=42)

models= {'의사결정나무':dt, '랜덤 포레스트':rf, '로지스틱 회귀':lr, '나이브 베이즈':gnb, 'KNN':knn, 'SVM':svc, '퍼셉트론':per, '확률적 경사하강법':sgd}

print('모델 학습을 시작합니다...')

fitting=[]
for model_name, model in models.items():
    for epoch in tqdm(range(100),desc='[Epoch 학습 중]'):
        model.fit(train_X, train_y)
        time.sleep(0.05)

print('모델 학습이 종료되었습니다...')

for model_name, model in models.items():
    pred=model.predict(test_X)
    acc=accuracy_score(test_y, pred)
    fitting.append([model_name,acc])


#===================================================================
# 3. 모델 비교

result=pd.DataFrame(fitting,columns=['모델명','정확도'])
result=result.sort_values(by='정확도',ascending=False)

result['정확도%']=(result['정확도']*100).round(2)
result = result.reset_index(drop=True)

print('\n')
print('--------------- 모델별 정확도 ---------------')
print(result[['모델명','정확도%']])


#===================================================================
# 4. 랜덤 포레스트 교차검증
from sklearn.model_selection import cross_val_score

scores = cross_val_score(rf,train_X,train_y,cv=5,scoring='accuracy')

print('\n----------랜덤 포레스트 교차검증----------')
print('각 검증 정확도:', scores)
print('평균 정확도:', round(scores.mean() * 100, 2), '%')