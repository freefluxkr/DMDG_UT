import pandas as pd
url = 'https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv'
df = pd.read_csv(url, sep='\t')

####### 최종 데이터 확인 #######
df['Rename'] = df['Name'].str.extract(r'([A-Za-z]+)\.') # 이름구분하기 알파벳시작 + . 으로 끝나는 이름들
print(df['Rename'].value_counts()) # 이름을 넘많음 5개로 구분하고 숫자형 데이터로 바꾸기

df['Rename'] = df['Rename'].replace(
    ['Dr','Rev','Major','Col','Capt','Sir','Jonkheer'],
    'Rare'
)
df['Rename'] = df['Rename'].map({
    'Mr':0,
    'Miss':1,
    'Mrs':2,
    'Master':3,
    'Rare':4
})
print(df['Rename'])

###### age 빈값을 호칭별 중앙값으로 바꾸기 결측치를 바꾸기

df['Age'] = df.groupby('Rename')['Age'].transform(lambda x: x.fillna(x.median()))
print(df['Age'])

df['Sex'] = df['Sex'].map({'male':0, 'female':1}) # 남녀 0 1 로 바꾸기
print(df['Sex'])

print(df['Embarked'].isnull().sum()) # 1개 결측치를 최빈값으로 채우고 숫자로 바꿈
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
print(df['Embarked'].value_counts()) # S C Q 최빈값 3개
df['Embarked'] = df['Embarked'].map({'S':0, 'C':1, 'Q':2})

df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['Fare_person'] = df['Fare'] / df['FamilySize']

df = df.drop(['PassengerId','Name','Ticket','Cabin'],
    axis=1) # 필요없는 열 제거

print(df.head())
print(df.info())

from sklearn.model_selection import train_test_split # 학습용과 테스트용으로 나누기 여기서테스트용은 20%
X = df.drop('Survived', axis=1) # 관례상 X 대문자, drop 정답열을 날려버림 남은컬럼으로 학습하도록함
y = df['Survived'] # 정답지를 가지고 있음
########### X y 데이터 학습 테스트 용 나눠주기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)

score = cross_val_score(
    model,
    X,
    y,
    cv=5
)

print(score)
print(f"평균 정확도: {score.mean():.4f}")












