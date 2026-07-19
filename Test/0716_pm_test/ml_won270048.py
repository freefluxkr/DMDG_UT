######################################################
###############      결        론         #############
# 총 8개의 분류 모델을 비교한 결과 LinearSVC가 87.5%로 가장 높은 정확도를
# 보였다. Random Forest와 Logistic Regression도 84.38%로 우수한 성능을
# 나타냈다. 반면 Decision Tree는 단일 트리 구조의 한계로 상대적으로 낮은
# 성능을 보였으며, KNN, Perceptron, SGDClassifier는 StandardScaler를
# 적용한 후 정확도가 크게 향상되었다.
##########################################################


import pandas as pd

df = pd.read_csv(r'C:\Users\enjoy\PycharmProjects\PythonProject\0714\titanic.txt', encoding='utf-8',sep='\t')
print(df.head())
print(df.shape)
print(df.isnull().sum())
#########################
##### 호칭 5개로 분류'
#########################
# 1. Name에서 호칭 추출
df['Title'] = df['Name'].apply(
    lambda x: x.split(',')[1].split('.')[0].strip()
)

# 2. 5개 그룹으로 분류
main_titles = ['Mr', 'Miss', 'Mrs', 'Master']

df['Title'] = df['Title'].apply(
    lambda x: x if x in main_titles else 'Rare'
)

# 3. 확인
print(df['Title'].value_counts())

# 4. 숫자로 변환
df['Title'] = df['Title'].map({
    'Mr': 0,
    'Miss': 1,
    'Mrs': 2,
    'Master': 3,
    'Rare': 4
})

#########################
##### Fair_person추가
#########################
df['Family_Size'] = df['SibSp'] + df['Parch'] + 1
df['Fare_Person'] = df['Fare'] / df['Family_Size']
print(df['Fare_Person'][0])
#########################
##### Age 결측치는 호칭별 중앙값으로 채우고, cabin은 유무만 표시, Embarked는 최빈값
#########################
#
df['Age'] = df['Age'].fillna(
    df.groupby('Title')['Age'].transform('median')
)
df['Has_Cabin'] = df['Cabin'].notnull().astype(float)
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df['Sex'] = df['Sex'].map({
    'female': 1,
    'male': 0
})
## male 0보다 female을 0으로 했을때 정확도가 더 높아진다 (왜지??)
df['Embarked'] = df['Embarked'].map({
    'S':0,
    'C':1,
    'Q':2
})

# 전처리 결과
print(df.isnull().sum())

#########################
##### 정답데이터와 테스트데이터
#########################

# 정답 데이터 - 생존
y = df['Survived']
# 분석 데이터
X = df[
    [
        'Pclass',
        'Sex',
        'Age',
        'SibSp',
        'Parch',
        'Fare',
        'Embarked',
        'Has_Cabin',
        'Title',
        'Fare_Person'
    ]
]

print(df.dtypes)


#########################
##### train_test_split
#########################
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Decision Tree :", accuracy_score(y_test, pred))


#########################
##### RandomFrest
#########################
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Random Forest :", accuracy_score(y_test, predictions))

#########################
##### GaussianNB
#########################
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("GaussianNB :", accuracy_score(y_test, predictions))


#########################
##### 데이터 스케일링
#########################

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#########################
##### LogisticRegression
#########################
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

model = LogisticRegression(
    C=1.0,
    solver='lbfgs',
    max_iter=1000,
    random_state=42
)

model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)

print("Logistic Regression :", accuracy_score(y_test, predictions))


#########################
##### KNeighborsClassifier
#########################
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5, metric='minkowski')
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)
print("KNeighborsClassifier :", accuracy_score(y_test, predictions))

#########################
##### LinearSVC
#########################
from sklearn.svm import LinearSVC
model = LinearSVC(C=1.0, random_state=42)
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)
print("LinearSVC :", accuracy_score(y_test, predictions))

#########################
##### Perceptron
#########################
from sklearn.linear_model import Perceptron
model = Perceptron(max_iter=1000, eta0=1.0, random_state=42)
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)
print("Perceptron :", accuracy_score(y_test, predictions))

#########################
##### SGDClassifier
#########################
from sklearn.linear_model import SGDClassifier
model = SGDClassifier(loss='log_loss', penalty='l2', random_state=42)
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)
print("SGDClassifier :", accuracy_score(y_test, predictions))