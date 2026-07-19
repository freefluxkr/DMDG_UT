import pandas as pd
import ssl
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import SGDClassifier


# 1. 데이터 로드
ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv'
df = pd.read_csv(url, sep='\t')

# [Name 구분] 호칭(Title) 추출 및 5개 그룹 숫자화
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
df['Title'] = df['Title'].replace('Mlle', 'Miss').replace('Ms', 'Miss').replace('Mme', 'Mrs')
df['Title'] = df['Title'].map({"Mr": 0, "Miss": 1, "Mrs": 2, "Master": 3, "Rare": 4})

# [Age 결측치] 호칭별 중앙값으로 채우기
df['Age'] = df.groupby('Title')['Age'].transform(lambda x: x.fillna(x.median()))

# [Sex 변환] 0, 1
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# [Embarked 변환]
df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).fillna(0)

# [가족 규모 및 1인당 요금] Fare_person 생성
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['Fare_person'] = df['Fare'] / df['FamilySize']

# 3. 모델 학습
features = ['Pclass', 'Sex', 'Age', 'Title', 'Embarked', 'FamilySize', 'Fare_person']
X = df[features]
y = df['Survived']

model = DecisionTreeClassifier(criterion='entropy', max_depth=4) # 복잡한 데이터를 잘 보게 깊이 4
model.fit(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

###### 4. 시각화 ######

# 1. 의사결정 나무

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
probs = model.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"의사결정 나무의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")

plt.figure(figsize=(25, 12))
plot_tree(model,
          feature_names=features,
          class_names=['Dead', 'Survived'],
          filled=True,
          rounded=True,
          fontsize=10)
plt.show()

# 2. 랜덤 포레스트
model_rf = RandomForestClassifier(n_estimators=100, criterion='entropy')
model_rf.fit(X_train, y_train)
probs = model_rf.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"랜덤 포레스트의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")

plt.figure(figsize=(30, 15))
plot_tree(model_rf.estimators_[0], feature_names=features, filled=True,fontsize=8)
plt.title("Random Forest (One Tree)")
plt.show()

# 3. 로지스틱 회귀분석
model_log = LogisticRegression(max_iter=1000)
model_log.fit(X_train, y_train)
probs = model_log.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"로지스틱 회귀분석의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")


# 4. 나이브 베이지안 모델

model_nb = GaussianNB()
model_nb.fit(X_train, y_train)
probs = model_nb.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"나이브 베이지안 모델의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")

# 5. K-Nearest Neighbor 모델


model = KNeighborsClassifier(n_neighbors=5, metric='minkowski')
model.fit(X_train, y_train)
probs = model.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"K-Nearest Neighbor 모델의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")

# 6. SVM(Support Vector Machine) 모델

base_model = SVC(kernel='linear',C=1.0, random_state=42)
model = CalibratedClassifierCV(base_model, ensemble=False)
model.fit(X_train, y_train)

probs = model.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"SVM 모델의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")

# 7. 퍼셉트론(Perceptron) 모델

base_model = Perceptron(max_iter=1000, eta0=1.0, random_state=42)
model = CalibratedClassifierCV(base_model, cv=5)
model.fit(X_train, y_train)

probs = model.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"퍼셉트론 모델의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")

# 8. 확률적 경사하강법(Stochastic Gradient Descent / SGDClassifier)

model = SGDClassifier(loss='log_loss', penalty='l2', random_state=42)
model.fit(X_train, y_train)
probs = model.predict_proba(X_test)
avg_survival_prob = probs[:, 1].mean()

print(f"확률적 경사하강법의 평균 생존 예측 확률: {avg_survival_prob * 100:.2f}%")