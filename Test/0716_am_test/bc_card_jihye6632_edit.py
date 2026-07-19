'''
Pandas 만 사용하여 문제 해결하기

카드 소비 데이터 분석
1. 원본 데이터 소개
2. 데이터 전처리
3. 데이터 분석

### 서울시 거주/비거주 고객의 소비 분석
## 1. 서울시 거주/비거주 고객 수 구하기
## 2. 총 소비액 구하기
## 3. 성별 소비액 구하기

### 편의점 소비 정보 분석
## 1. 편의점 소비액 구하기
## 2. 강남구 편의점 소비액 구하기

'''

############
# 원본 데이터 소개
#############

# 본인 컴퓨터에서 모든 파일이 교수님의 코드를 사용하여도 무한로딩이 끝나지 않아
# 클로드의 도움을 받아 파일 가공 후 진행

import pandas as pd

df = pd.read_csv("../data/bc_card.txt",encoding='utf-8',sep='\t')

print(df.head())
print(df.tail())
print(df.info())

'''
정상확인
'''

# 데이터 전처리
print(df.isnull().sum())

'''
결측치 없는 것으로 보임. 분석진행
print(df.isnull().sum())
REG_YYMM             0
MEGA_CTY_NO          0
MEGA_CTY_NM          0
CTY_RGN_NO           0
CTY_RGN_NM           0
ADMI_CTY_NO          0
ADMI_CTY_NM          0
MAIN_BUZ_CODE        0
MAIN_BUZ_DESC        0
TP_GRP_NO            0
TP_GRP_NM            0
TP_BUZ_NO            0
TP_BUZ_NM            0
CSTMR_GUBUN          0
CSTMR_MEGA_CTY_NO    0
CSTMR_MEGA_CTY_NM    0
CSTMR_CTY_RGN_NO     0
CSTMR_CTY_RGN_NM     0
SEX_CTGO_CD          0
AGE_VAL              0
FLC                  0
AMT                  0
CNT                  0
dtype: int64
'''

###################################

### 서울시 거주/비거주 고객의 소비 분석
## 1. 서울시 거주/비거주 고객 수 구하기
'''
사용 필요 컬럼?
CSTMR_MEGA_CTY_NO : 고객 거주지의 광역시·도 코드 (예: 11) — bc_card_output.txt
CSTMR_MEGA_CTY_NM : 고객 거주지의 광역시·도명 (예: 서울특별시) — bc_card_output.txt
'''

city=list(df['CSTMR_MEGA_CTY_NM'].unique())
city1=list(df['CSTMR_MEGA_CTY_NM'])

def people_count(t):
    if t == "서울특별시":
        return 1
    else:
        return 0

df["카드이용객"]= df['CSTMR_MEGA_CTY_NM'].apply(people_count)

seoul_count=df["카드이용객"].sum()
noseoul_count=len(df)-seoul_count

#---- 서울 거주자 고객 수
print("서울 거주 고객: ",seoul_count,"명")
'''
서울 거주 고객:  54150 명
'''
#---- 서울 비거주자 고객 수
print("서울 비거주 고객: ",noseoul_count,"명")
'''
서울 비거주 고객:  45851 명
'''

## 2. 총 소비액 구하기
total_amt=df["AMT"].sum()

print(f"총 소비액: {total_amt:,}원")
'''
총 소비액: 266,250,278,498원
'''


## 3. 성별 소비액 구하기
'''
SEX_CTGO_CD
'''

gender_amt = df["AMT"].groupby(by=df["SEX_CTGO_CD"]).sum()

print(f"남성 소비액: {gender_amt[1]:,}원")
print(f"여성 소비액: {gender_amt[2]:,}원")
'''
남성 소비액: 131,707,949,762원
여성 소비액: 134,542,328,736원
'''




##################################################
### 편의점 소비 정보 분석

## 1. 편의점 소비액 구하기
conv_amt = df["AMT"].groupby(by=df["TP_BUZ_NM"]).sum()
print(f"편의점 소비액: {conv_amt['편 의 점']:,}원")

'''
편의점 소비액: 7,299,184,098원
'''

## 2. 강남구 편의점 소비액 구하기

conv_merge = df["AMT"].groupby(by=[df["CTY_RGN_NM"], df["TP_BUZ_NM"]]).sum()
print(f"강남구 편의점 소비액: {conv_merge['강남구', '편 의 점']:,}원")
'''
강남구 편의점 소비액: 707,275,140원
'''