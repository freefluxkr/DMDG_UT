import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
url = 'https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv'
df = pd.read_csv(url, sep='\t')

print(df.head())
print(df.info())
print(df.describe())
df = df[(df.Survived > -1) & (df.Survived < 2)] # 생존여부 0 1 만 추출
df = df[['Survived','Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']] # 필요한 컬럼만 사용
df['Age'] = df['Age'].fillna(df['Age'].mean()) # 빈값에 나이 평균을 집어넣음
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0]) # 나이는 결측치 평균넣고 항구는 평균못구함 최빈값을 넣어줌 가장많이 나온값 0번째 값
df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True) # 문자열숫자로 0과1로 데이터기준나눔 드랍퍼스트 트루 값이3개는 중복하나제거

print(df.head())

from sklearn.model_selection import train_test_split # 학습용과 테스트용으로 나누기 여기서테스트용은 20%
X = df.drop('Survived', axis=1) # 관례상 X 대문자, drop 정답열을 날려버림 남은컬럼으로 학습하도록함
y = df['Survived'] # 정답지를 가지고 있음
########### X y 데이터 학습 테스트 용 나눠주기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score ######################################################### 의사결정나무

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train) # 학습할자료를 공부시키기
pred = model.predict(X_test) # X야 테스트 보자 시험지 주고 시험시키기

print("DecisionTree 정확도는", accuracy_score(y_test, pred))

from sklearn.ensemble import RandomForestClassifier ################################################ 랜덤포레스트

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('RandomForestClassifier 정확도는', accuracy_score(y_test, pred))

from sklearn.neighbors import KNeighborsClassifier ################################################## KNN

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print('KNN 정확도는', accuracy_score(y_test, pred))

from sklearn.linear_model import LogisticRegression ################################################# 로지스틱 회귀

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('로지스틱 회귀 정확도는', accuracy_score(y_test, pred))

from sklearn.svm import SVC ######################################################################### SVM

model = SVC()
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('SVM 정확도는', accuracy_score(y_test, pred))

from sklearn.naive_bayes import GaussianNB ########################################################### 나이브베이즈

model = GaussianNB()
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('나이브 베이즈 정확도는', accuracy_score(y_test, pred))

from sklearn.linear_model import Perceptron ############################################################# 퍼셉트론

model = Perceptron(random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('퍼셉트론 정확도는', accuracy_score(y_test, pred))

from sklearn.linear_model import SGDClassifier

model = SGDClassifier(loss="log_loss", random_state=42 )
model.fit(X_train, y_train)
pred = model.predict(X_test)
print('SGD 확률적 경사하강법 정확도는', accuracy_score(y_test, pred))

models = {
'DecisionTree' : DecisionTreeClassifier(random_state=42),
'RandomForestClassifier' : RandomForestClassifier(random_state=42),
'KNN' : KNeighborsClassifier(n_neighbors=5),
'로지스틱 회귀' : LogisticRegression(max_iter=1000),
'SVM' : SVC(),
'나이브 베이즈' : GaussianNB(),
'퍼셉트론' : Perceptron(random_state=42),
'SGD 확률적 경사하강법' : SGDClassifier(loss="log_loss", random_state=42 )
}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print(name, ':', round(accuracy_score(y_test, pred), 4)) # 모델별 정확도 테스트 
















