!pip install scikit-learn pandas numpy

import pandas as pd
import numpy as np

# 머신러닝 모델 라이브러리 불러오기
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import Perceptron, SGDClassifier

# 평가 및 데이터 분할 라이브러리 불러오기
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

import warnings
warnings.filterwarnings('ignore') # 실행 시 나타나는 경고 메시지 숨기기

# ==========================================
# 1. 데이터 불러오기
# ==========================================
print("1. 데이터를 불러오는 중입니다...")
url = "https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv"
df = pd.read_csv(url, sep='\t')

# ==========================================
# 2. 데이터 전처리 (사전 작업)
# ==========================================
print("2. 데이터 전처리(사전 작업)를 시작합니다...")

# [1] Name(이름) 열에서 호칭(Title)을 추출하고 5개로 구분하여 숫자로 바꾸기
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)

# 주요 4대 호칭 외에는 모두 'Other(4)'로 통합 및 수치화
title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2, "Master": 3}
df['Title'] = df['Title'].map(title_mapping).fillna(4)

# [2] Age(나이) 열의 빈 값을 호칭(Title)별 중앙값(Median)으로 바꾸기
df["Age"] = df.groupby("Title")["Age"].transform(lambda x: x.fillna(x.median()))

# [3] Sex(성별) 열에서 'male': 0, 'female': 1로 바꾸기
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# [4] Embarked(탑승 항구) 빈 값을 최빈값으로 채우고 수치화하기
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# [5] SibSp(형제자매/배우자), Parch(부모/자녀) 열을 합쳐 가족 크기 생성 및
# Fare(요금) 열을 이용하여 개인별 요금(Fare_person) 열 추가하기
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['Fare_person'] = df['Fare'] / df['FamilySize']

# [6] 최종 데이터 확인 및 불필요한 열 제거
df_clean = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])

# 입력 데이터(X)와 정답 데이터(y, 생존 여부) 나누기
X = df_clean.drop(columns=['Survived'])
y = df_clean['Survived']

# 데이터를 학습용(80%)과 검증용(20%)으로 분할하기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"-> 전처리 완료! 사용된 특성(Column): {list(X.columns)}")
print("-" * 60)

# ==========================================
# 3. 다양한 머신러닝 모델 적용 및 학습
# ==========================================
print("3. 머신러닝 모델을 학습하고 정확도를 비교합니다...")

models = {
    "의사결정 나무 (Decision Tree)": DecisionTreeClassifier(random_state=42),
    "랜덤 포리스트 (Random Forest)": RandomForestClassifier(random_state=42),
    "로지스틱 회귀 (Logistic Regression)": LogisticRegression(max_iter=1000, random_state=42),
    "나이브 베이지안 (Gaussian NB)": GaussianNB(),
    "K-최근접 이웃 (KNN)": KNeighborsClassifier(),
    "SVM (LinearSVC)": LinearSVC(max_iter=5000, random_state=42),
    "퍼셉트론 (Perceptron)": Perceptron(random_state=42),
    "확률적 경사하강법 (SGD Classifier)": SGDClassifier(random_state=42)
}

# 각 모델의 정확도를 저장할 딕셔너리
results = {}

for name, model in models.items():
    # 모델 학습
    model.fit(X_train, y_train)
    # 예측하기
    pred = model.predict(X_test)
    # 정확도 평가
    acc = accuracy_score(y_test, pred)
    results[name] = acc
    print(f"- {name:<30} 정확도: {acc:.4f}")

print("-" * 60)

# 가장 성능이 좋은 모델 출력
best_model = max(results, key=results.get)
print(f" 가장 높은 정확도를 보여주는 모델: {best_model} ({results[best_model]:.4f})")
print("-" * 60)

# ==========================================
# 4. 랜덤 포리스트 모델의 교차검증 (Cross Validation)
# ==========================================
print("4. 랜덤 포리스트 모델의 교차검증을 실시합니다 (5-Fold)...")

# 전체 데이터(X, y)에 대해 5겹 교차검증 수행
rf_model = RandomForestClassifier(random_state=42)
scores = cross_val_score(rf_model, X, y, cv=5)

print(f"- 각 5회차별 정확도: {scores}")
print(f"- 교차검증 평균 정확도: {scores.mean():.4f}")
print("=" * 60)
print("예측 프로젝트 프로세스가 성공적으로 완료되었습니다!")