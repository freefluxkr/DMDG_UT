import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# TODO : Predict Survival Rate
#Compare reliability
#Final result confirm

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier

import urllib.request
import os

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

file_path = 'titanic.csv'
url = 'https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv'

#file_path에 지정한 파일을 불러오기
#해당 파일이 없으면 url에서 다운로드
def prepare_csv_data():
  if not os.path.exists(file_path):
    print('FILE DOWNLOAD\n')
    try:
      urllib.request.urlretrieve(url, file_path)
      print('DOWNLOADED\n')
    except Exception as e:
      return None

  data = pd.read_csv(file_path, encoding='utf-8', sep='\t')
  return data

#데이터 전처리
def check_preprocessing(_data):
    #print('\n>>>DESC<<<\n',data.describe())
    #print('\n>>>INFO<<<\n',data.info())
    """
    #>>>INFO<<<
    <class 'pandas.DataFrame'>
    RangeIndex: 156 entries, 0 to 155
    Data columns (total 12 columns):
     #   Column       Non-Null Count  Dtype
    ---  ------       --------------  -----
     0   PassengerId  156 non-null    int64
     1   Survived     156 non-null    int64
     2   Pclass       156 non-null    int64     #1, 2, 3
     3   Name         156 non-null    str
     4   Sex          156 non-null    str
     5   Age          126 non-null    float64   #estimated ages exist
     6   SibSp        156 non-null    int64     #sibling & spouse
     7   Parch        156 non-null    int64     #parent & child
     8   Ticket       156 non-null    str       #Ticket number
     9   Fare         156 non-null    float64
     10  Cabin        31 non-null     str
     11  Embarked     155 non-null    str
    dtypes: float64(2), int64(5), str(5)

    CAUTION:
    1. Age, Cabin, Embarked에서 결측치 발견
    2. Sex는 문자열('male','female')
    """

    #필요없는 컬럼 삭제
    _data = _data.drop(['PassengerId','Pclass','Name','Ticket','Cabin', 'Embarked'], axis=1)

    #성별을 숫자로 변환
    _data['Sex'] = _data['Sex'].replace({'male':1,'female':0}).astype(int)

    #나이의 결측치를 중앙값으로 변경
    _data['Age'] = _data['Age'].fillna(_data['Age'].median())

    # print('\n>>>DESC<<<\n',_data.describe())
    # print('\n>>>INFO<<<\n',_data.info())
    '''
    >>>
    RangeIndex: 156 entries, 0 to 155
    Data columns (total 6 columns):
     #   Column    Non-Null Count  Dtype  
    ---  ------    --------------  -----  
     0   Survived  156 non-null    int64  
     1   Sex       156 non-null    int64  
     2   Age       156 non-null    float64
     3   SibSp     156 non-null    int64  
     4   Parch     156 non-null    int64  
     5   Fare      156 non-null    float64
    dtypes: float64(2), int64(4)
    
    RESULT:
    1. 필요없는 칼럼 제외 완료
    2. Age의 결측치 변경 완료
    3. Sex의 데이터 타입 변경 완료
    
    POTENTIAL:
    1. Fare의 수치가 상대적으로 높기 때문에 Scale 적용 예정
    '''
    return _data

#학습(훈련)용/테스트용 데이터 분리
def split_data(_data):
    features = ['Sex', 'Age','SibSp','Parch','Fare']
    target = 'Survived'

    X, y = _data[features], _data[target]

    #모델 비교를 위해 데이터 분할 시, 무작위성 제거
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

#Fare와 다른 수치들을 Scale해서 학습(훈련)에 용이하도록 변경
def scale_data(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    #학습 데이터와 실제 예측용 데이터의 기준(평균, 표준편차)이 달라질 수 있기 때문에 fit을 하지 않음
    X_test_scaled  = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler

#8개의 모델을 비교하기 위해 랜덤치를 고정해서 학습(훈련)
def train_model(_X, _y):
    models = [
        DecisionTreeClassifier(random_state=42),
        RandomForestClassifier(random_state=42),
        LogisticRegression(random_state=42),
        LinearSVC(random_state=42),
        Perceptron(random_state=42),
        SGDClassifier(random_state=42),
        GaussianNB(),
        KNeighborsClassifier()]

    for model in models:
        model.fit(_X, _y)

    return models

#학습(훈련)한 모델들의 결과값을 테스트(정답과 비교)
def evaluate_models(_models, _X_train, _X_test, _y_train, _y_test):
    _records = []

    print('\nModel Performance')
    for model in _models:
        predictions = model.predict(_X_test)

        #테스트 신뢰도를 높이기 위한 교차검증 실행
        cross_scores = cross_val_score(model, _X_train, _y_train, cv=5)
        score = accuracy_score(_y_test, predictions)
        name = model.__class__.__name__

        print(f'\n{name}'
              f'\nInitial Score     : {score*100}%'
              f'\nCross Score(Mean) : {round(cross_scores.mean()*100, 2)}%'
              f'\nCross Score(STD)  : {round(cross_scores.std(), 3)}')

        _records.append({
            'Model': name,
            'Initial Score'    : round(score*100, 2),               #Initial Score
            'Cross Score(Mean)': round(cross_scores.mean()*100, 2), #Mean Score(교차검증 평균)
        })

    return pd.DataFrame(_records)

#시각화
def visualize_results(_data):
    _values = _data.melt(
        id_vars=['Model'],
        value_vars=['Initial Score', 'Cross Score(Mean)'],
        var_name='Metric',
        value_name='Score'
    )

    # 참고 코드처럼 팔레트를 변수로 분리해서 관리
    pal = {'Initial Score': '#4C72B0', 'Cross Score(Mean)': '#DD8452'}

    plt.figure(figsize=(12, 6))
    pl = sns.barplot(data=_values, x='Model', y='Score', hue='Metric', palette=pal)
    pl.set_title('Model Performance')

    for container in pl.containers:
        pl.bar_label(container, fmt='%.1f', fontsize=8, padding=2)

    pl.set_xlabel('Model')
    pl.set_ylabel('Score (%)')
    plt.legend(bbox_to_anchor=(0, 1.15), loc='upper left')
    plt.xticks(rotation=7, ha='center')
    plt.show()

#데이터 불러오기부터 차례대로 실행
def main():
    data_processed = check_preprocessing(prepare_csv_data())
    X_train, X_test, y_train, y_test = split_data(data_processed)
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)

    #Scale한 X 데이터를 파라미터로 할당
    model_train = train_model(X_train_scaled, y_train)
    result_data = evaluate_models(model_train, X_train_scaled, X_test_scaled, y_train, y_test)
    visualize_results(result_data)

#TODO:
# 함수 실행
main()
'''
>>>
Model Performance

DecisionTreeClassifier
Initial Score     : 75.0%
Cross Score(Mean) : 74.23%
Cross Score(STD)  : 0.058

RandomForestClassifier
Initial Score     : 71.875%
Cross Score(Mean) : 78.23%
Cross Score(STD)  : 0.018

LogisticRegression
Initial Score     : 71.875%
Cross Score(Mean) : 81.43%
Cross Score(STD)  : 0.065

LinearSVC
Initial Score     : 68.75%
Cross Score(Mean) : 82.23%
Cross Score(STD)  : 0.055

Perceptron
Initial Score     : 62.5%
Cross Score(Mean) : 66.17%
Cross Score(STD)  : 0.073

SGDClassifier
Initial Score     : 68.75%
Cross Score(Mean) : 77.33%
Cross Score(STD)  : 0.082

GaussianNB
Initial Score     : 71.875%
Cross Score(Mean) : 77.37%
Cross Score(STD)  : 0.076

KNeighborsClassifier
Initial Score     : 65.625%
Cross Score(Mean) : 83.83%
Cross Score(STD)  : 0.058

RESULT:
초기 테스트값에서는 결정트리가 75.0으로 가장 높은 성능을 보였지만,
교차검증을 5회 시행한 값의 평균은 K-최근접 이웃이 83.8로 가장 높은 교차검증 평균값을 보였다.

초기 테스트 값과 교차검증 평균값의 차이가 가장 큰 모델은 K-최근접 이웃으로 13.4 포인트의 차이가 났다.
초기 테스트 값과 교차검증 평균값의 차이가 가장 적은 모델은 결정 트리로 0.8 포인트의 차이가 났다.

퍼셉트론의 경우, 초기 테스트값과 교차검증 평균값에서 모두 가장 낮은 성능을 보였다.

ANALYSIS:
초기 테스트값과 교차검증 평균값의 차이가 10정도로 크게 벌어진
선형회귀, 선형 서포트 벡터 분류, 확률적 경사 하강법, K-최근접 이웃은 훈련(학습)에 많은 데이터가 필요하다는 것을 알 수 있다.

그 외에도 랜덤 포레스트, 가우시안 나이브 베이즈도 교차검증 평균값이 높게 나왔기 때문에
학습(훈련)에 보다 더 많은 데이터가 필요하다는 것을 알 수 있다. 

결정 트리의 경우, 초기 테스트값과 교차검증 평균값이 유사하기 때문에
훈련(학습)에 필요한 데이터가 적더라도 일정한 결과값을 얻는다는 것을 알 수 있다.

전체적으로 데이터의 개수가 156개밖에 안되기 때문에,
충분하게 신뢰성있는 훈련(학습)이 되지 못한 것을 알 수 있다.
'''