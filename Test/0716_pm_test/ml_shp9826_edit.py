import ssl
ssl._create_default_https_context = ssl._create_unverified_context
'''
컬럼의미값/비고
PassengerId승객 고유 번호단순 인덱스, 예측에 무의미
Survived생존 여부 (타겟 변수)0 = 사망, 1 = 생존
Pclass티켓 등급 (Passenger Class)1 = 1등석, 2 = 2등석, 3 = 3등석. 사회경제적 지위 proxy
Name이름문자열. Mr/Mrs/Miss/Master 등 호칭(Title) 추출에 자주 씀
Sex성별male / femaleAge나이결측치 존재 (약 20%)
SibSp함께 탑승한 형제자매 + 배우자 수Sibling + Spouse
Parch함께 탑승한 부모 + 자녀 수Parent + Child
Ticket티켓 번호문자+숫자 혼재, 형식 불규칙
Fare운임 요금연속값. 결측 거의 없음(test에 1건)
Cabin객실 번호결측치 매우 많음 (약 77%)
Embarked탑승 항구C = Cherbourg, Q = Queenstown, S = Southampton. 결측 소수
'''

#rand, deci << 높은 정확

import pandas as pd
from sklearn.metrics import accuracy_score

def name_for_num(name):
    tmp = name.split(',')[1]
    tmp = tmp.removeprefix(' ')
    slited_name = tmp.split('.')[0]
    if slited_name[0] == 'Mr':
        return 1
    elif slited_name[0] == 'Mrs':
        return 2
    elif slited_name[0] == 'Miss':
        return 3    
    elif slited_name[0] == 'Master':
        return 4
    return 5 #Don
    
def sex_for_num(str):
    if str =='male':
        return 0
    return 1

def name_dis(name_ser):
    return name_ser.apply(name_for_num)
    
def em_func(str):
    if str == 'C':
        return 1
    elif str == 'Q':
        return 2
    return 3

def convert_embarked(em):
    pass
    return em.apply(em_func)

def fill_age_miss_val(df):
    print(f"age na:\n {df['Age'].isna().sum()}") #- 30개의 결측치
    print('#'*30)
    return df['Age'].fillna(df['Age'].median()) #나이의 결측치를 중앙 값으로 채우기

def sex_num_by_sex(ser):
    return ser.apply(sex_for_num)

def prepared():
    # num_to_preFix = {1:'Mr', 2:'Mrs', 3:'Miss',4:'Master',5:'Don'} #이거는 문제 풀이에 1도 상관x 디버깅용

    df = pd.read_csv("https://raw.githubusercontent.com/sehakflower/data/main/titanic.csv", sep='\t')
    print(df.describe())
    print(df.isna().sum()) #결측치 확인
    # Cabin이 결측이 개많은데?
    # print(df.head())
    # return
    # for ele in df.columns:
    #     print(f"{ele}: {df[ele].isna().sum()}")
        
    # return
    # print(df.groupby('Embarked').count()) #C Q S 임을 확인
    df['Name_alias'] = name_dis(df['Name']) #이름은 string이니까, Mr이런거에 대한 매칭되는 숫자 바꿔주기
    
    df.dropna(subset=['Embarked'])#결측치 하나 날리기

    # 2
    df['Age'] = fill_age_miss_val(df)

    # 3
    df['Sex'] = sex_num_by_sex(df['Sex'])
    print(f"apply sex:\n {df.head()}") # Name_code 확인
    print('#'*30)

    # 4 ~ 5
    # 형제 부모는 영향을 줄까?
    # 상관 관계를 봐야할까?
    # par_df = df[['Survived','Parch']]
    # sib_df = df[['Survived','SibSp']]
    # print(par_df.corr(method='pearson'))
    # print(par_df.corr(method='spearman'))
    # print(par_df.corr(method='kendall'))
    # print(sib_df.corr(method='pearson'))
    # print(sib_df.corr(method='spearman'))
    # print(sib_df.corr(method='kendall'))


    '''
              Survived     Parch
    Survived  1.000000  0.039435
    Parch     0.039435  1.000000
              Survived     Parch
    Survived  1.000000  0.031816
    Parch     0.031816  1.000000
              Survived     Parch
    Survived  1.000000  0.030834
    Parch     0.030834  1.000000
              Survived     SibSp
    Survived  1.000000 -0.066943
    SibSp    -0.066943  1.000000
              Survived     SibSp
    Survived  1.000000 -0.008724
    SibSp    -0.008724  1.000000
              Survived     SibSp
    Survived  1.000000 -0.008344
    SibSp    -0.008344  1.000000

    각 0.03, -0.06을 가져서, 관계가 없는걸로 판단되어 drop
    '''
    df = df.drop(labels='Parch', axis=1) # 생존 예측에 이 번호는 필요 없음
    df = df.drop(labels='SibSp', axis=1) # 생존 예측에 이 번호는 필요 없음
    

    # 시작 위치는 생존과 크게 관련 없어보임
    #df['Embarked'] = convert_embarked(df['Embarked']) #문자 -> 숫자
    df = df.drop(labels='Embarked', axis=1) # 생존 예측에 이 번호는 필요 없음

    # 6 - 이름으로 지불 가격 합/평균(어떤걸 원하는지.. groupby로 다른 col까지 더 묶어서 했어야했나...싶기도)
    # "개인별 요금 나타내는 fare_person" = 티켓 총액을 그 티켓 공유 인원수로 나눈 값.
    # fare_person = Fare / (그 티켓을 함께 쓴 사람 수)


    print(f"Na Value:\n{df.isna().sum()}")
    print(df.info())
    
    df['n_on_ticket'] = df.groupby('Ticket')['Ticket'].transform('count')# 티켓 그룹 - 같은 티켓 카운트
    df['fare_person'] = df['Fare'] / df['n_on_ticket'] #내 가격을 같은 티켓산 사람끼리 n빵

    print(f"apply fare info:\n {df.head()}")
    print('#'*30)

    df = df.drop(labels='PassengerId', axis=1) # 생존 예측에 이 번호는 필요 없음
    df = df.drop(labels='Name', axis=1) # 생존에 관해서 이름은 연관이 1도 없어서 drop
    df = df.drop(labels='Ticket', axis=1) # 티켓도 의미 없으니 drop
    df = df.drop(labels='Cabin', axis=1) # 125/156일 정도로 결측치가 많아서 drop

    print("Droped Null")
    print(f"Na Value:\n{df.isna().sum()}")
    print(df.info())
    '''
    Na Value:
    Survived            0
    Pclass              0
    Sex                 0
    Age                 0
    SibSp               0
    Parch               0
    Fare                0
    Embarked            0
    Name_alias          0
    fare_person_sum     0
    fare_person_mean    0

    <class 'pandas.DataFrame'>
    RangeIndex: 156 entries, 0 to 155
    Data columns (total 11 columns):
     #   Column            Non-Null Count  Dtype  
    ---  ------            --------------  -----  
     0   Survived          156 non-null    int64  
     1   Pclass            156 non-null    int64  
     2   Sex               156 non-null    int64  
     3   Age               156 non-null    float64
     4   SibSp             156 non-null    int64  
     5   Parch             156 non-null    int64  
     6   Fare              156 non-null    float64
     7   Embarked          156 non-null    int64  
     8   Name_alias        156 non-null    int64  
     9   fare_person_sum   156 non-null    float64
     10  fare_person_mean  156 non-null    float64

     non-null 확인
    '''

    return df    

# 각 모델들 학습 및 테스트 수행
def analyze_by_deci(train_X, train_y, test_X, test_y):
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result


def analize_by_rand(train_X, train_y, test_X, test_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

def analize_by_logic(train_X, train_y, test_X, test_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(C=1.0, penalty='l2', solver='lbfgs', random_state=42)
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

def analize_by_gaus(train_X, train_y, test_X, test_y):
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

def analize_by_knei(train_X, train_y, test_X, test_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=5, metric='minkowski')
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

def analize_by_linearSVC(train_X, train_y, test_X, test_y):
    from sklearn.svm import LinearSVC
    model = LinearSVC(C=1.0, random_state=42)
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

def analize_by_percept(train_X, train_y, test_X, test_y):
    from sklearn.linear_model import Perceptron
    model = Perceptron(max_iter=1000, eta0=1.0, random_state=42)

    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

def analize_by_SGD(train_X, train_y, test_X, test_y):
    from sklearn.linear_model import SGDClassifier
    model = SGDClassifier(loss='log_loss', penalty='l2', random_state=42)
    model.fit(train_X, train_y)#학습
    
    predictions = model.predict(test_X)
    result = accuracy_score(test_y, predictions)
    print(result)
    return result

# 모든 모델에 대해서 0~-5까지 학습, back 5개 테스트 수행
def analyze_ml(df):
    # df에서 survive를 뜯어야 함
    train_size = int(len(df)*0.8) # 8:2 비율로 학습/시험을 수행한다.

    train_X = df[:train_size]#학습
    train_y = train_X['Survived'] 
    train_X = train_X.drop(labels='Survived', axis=1) # 정답을 drop


    test_X = df[train_size:]#학습
    test_y = test_X['Survived']
    test_X = test_X.drop(labels='Survived', axis=1) #정답 drop


    result = { #각각의 result를 dict에 담는데
        #k : v
        'deci':  analyze_by_deci(train_X,train_y, test_X, test_y),
        'rand':  analize_by_rand(train_X,train_y, test_X, test_y),
        'logic':  analize_by_logic(train_X,train_y, test_X, test_y),
        'gaus':  analize_by_gaus(train_X,train_y, test_X, test_y),
        'knei':  analize_by_knei(train_X,train_y, test_X, test_y),
        'svc':  analize_by_linearSVC(train_X,train_y, test_X, test_y),
        'percept':  analize_by_percept(train_X,train_y, test_X, test_y),
        'sgd':  analize_by_SGD(train_X,train_y, test_X, test_y)
    }
    
    #result = list(result)
    import operator
    #result.sort(key = operator.itemgetter(1), reverse=True)
    sorted_result = sorted(result.items(), key = operator.itemgetter(1), reverse=True)
    print('[', '*'*5,'순위','*'*5,']')
    for res in sorted_result:
        print(res)


if __name__ == '__main__':
    df = prepared() # 결측치확인 및 생존에 관련 없는 컬럼 drop 작업
    analyze_ml(df)

'''
1. 테스트 표본이 부족하다.
 - test가 32개뿐이라 한 개 맞고 틀리고가 0.03125(3.1%)씩 움직임.
 
2. percept, knei, sgd, svc << 스케일 민감한 모델
 - sex컬럼의 값은 0,1이지만, Fare는 0~263이라는 값을 가지게 됨. => 범위가 100배 넘게 차이나는게 핵심 원인

3. 스케일이에 무관한 모델
 - 의사트리, 랜덤 숲 << 임계 값 기준 분기 -> 스케일 무관
 - 가우시안 << 피쳐별 분포 추정 -> 스케일 영향 적음

=> 컬럼간의 데이터 크기 스케일 차이가 작다면 2번 케이스의 모델을 사용해도 됨
'''