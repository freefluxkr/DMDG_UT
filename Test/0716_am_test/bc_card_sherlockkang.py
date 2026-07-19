'''
#Credit Card Usage Analysis
Use Pandas ONLY

1. 원본 데이터 소개
2. 데이터 전처리
3. 데이터 분석

#서울시 거주/비거주 고객의 소비 분석
서울시 거주/비거주 고객수 구하기
총 소비액 구하기
성별 별 소비액

#편의점 소비 정보 분석
편의점 소비액
강남구 편의점 소비액
서울시 거주/비거주 고객의 소비액
거주지 소재 편의점 소비액 구하기
'''
import pandas as pd

data = pd.read_csv('./data/bc_card_out2020_03.txt',sep='\t',encoding='utf-8')

#불러온 데이터의 head() 값 확인
# print(data.head())
'''
>>>
   REG_YYMM  MEGA_CTY_NO MEGA_CTY_NM  CTY_RGN_NO  ... AGE_VAL  FLC       AMT   CNT
0    202003           11       서울특별시        1168  ...     20대    1   7927440  1089
1    202003           11       서울특별시        1129  ...     40대    4    274100    25
2    202003           11       서울특별시        1144  ...  60대 이상    5  34395725   808
3    202003           11       서울특별시        1126  ...     20대    1  31860800  3699
4    202003           11       서울특별시        1168  ...     50대    4   2546487    45
'''

# 칼럼 및 데이터값 확인
# data.info()
# data.describe()
'''
>>> RangeIndex: 1589494 entries, 0 to 1589493
>>> Data columns (total 23 columns)
>>> dtypes: int64(13), str(10)
'''

# 결측치 확인
# print(data.isnull().sum())
'''
>>>
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

#분석에 필요한 컬럼만 추출
##가맹점 도시코드(서울=11), 가맹점 업종코드(편의점=4010), 가맹점 시군구 코드(강남구=1168), 고객 거주도시 코드(int), 고객 성별코드(1,2), 소비액(int)
data = data[['MEGA_CTY_NO','TP_BUZ_NO','CTY_RGN_NO','CSTMR_MEGA_CTY_NO','SEX_CTGO_CD','AMT']]
'''
MEGA_CTY_NO        : 가맹점 광역시도 코드       int
TP_BUZ_NO          : 가맹점 업종분류 코드       int
CTY_RGN_NO         : 가맹점 시군구 코드         int
CSTMR_MEGA_CTY_NO  : 고객 거주지 광역시도코드    int
SEX_CTGO_CD        : 고객 성별 코드            int
AMT                : 총 이용 금액              int
'''
#결과값을 저장할 데이터프레임 선언
result = pd.DataFrame()
result_gender = pd.DataFrame()

# 1. 거주지에 따라 서울/비서울 고객 분류
# 2. 총 소비액과 비율 계산
data['Region'] = data['CSTMR_MEGA_CTY_NO'].apply(lambda x: '서울' if x == 11 else '비서울')
result['Total spent'] = data.groupby('Region')['AMT'].sum()
result['Spent Ratio(%)'] = ((result['Total spent'] / result['Total spent'].sum()) * 100).round(2)

# 3. 거주지와 성별에 따라 고객 분류
# 4. 총 소비액과 비율 계산
result_gender['Total spent'] = data.groupby(['Region','SEX_CTGO_CD'])['AMT'].sum()
result_gender['Spent Ratio(%)'] = ((result_gender['Total spent'] / result_gender['Total spent'].sum()) * 100).round(2)

result_gender = result_gender.reset_index()

#성별 데이터 출력값 변경 (1,2 => '남자','여자')
result_gender['SEX_CTGO_CD'] = result_gender['SEX_CTGO_CD'].replace({1:'남자',2:'여자'})

# 결과값 칼럼 변경 ('SEX_CTGO_CD' => 'GENDER')
result_gender.rename(columns={'SEX_CTGO_CD':'GENDER'}, inplace=True)


# print(result)
'''
>>>
          Total spent  Spent Ratio(%)
Region                               
비서울     1940899349900           58.34
서울      1385914569631           41.66

ANALYSIS :
서울에 거주하지 않는 사람들의 소비가 조금 더 높다는 것을 알 수 있음.
생필품이나 가전가구보다는 간단한 식품이나 일상용품의 소비가 높을 것으로 예상.
소비패턴과 관련된 분석과 마케팅 필요.
'''

# print(result_gender)
'''
>>>
  Region GENDER    Total spent  Spent Ratio(%)
0    비서울     남자  1015425463575           30.52
1    비서울     여자   925473886325           27.82
2     서울     남자   682678945342           20.52
3     서울     여자   703235624289           21.14

ANALYSIS :
비서울 인구의 경우에는 남자, 서울 인구의 경우에는 여자가 소비율이 높다는 것을 알 수 있음.
서울 인구의 경우 의미있는 차이는 아니지만, 비서울 인구의 경우 차이가 좀 더 있음.
각 거주지역에 따른 남녀 상품의 진열, 홍보 비율을 조정하는 방안 분석 필요.
'''

#편의점 소비 정보 분석

# 0. 편의점 분류 데이터 추출
convi_data = data[data['TP_BUZ_NO'] == 4010]

# 1. 편의점 소비액
convi_total = pd.DataFrame({'Total spent': [convi_data['AMT'].sum()]})
print(convi_total)
'''
>>>
   Total spent
0  79987167291
'''

# 2. 강남구 편의점 소비액
convi_gangnam = convi_data[convi_data['CTY_RGN_NO'] == 1168]
cvs_gangnam_total = pd.DataFrame({'Total spent': [convi_gangnam['AMT'].sum()]})
print(cvs_gangnam_total)
'''
>>>
   Total spent
0   8170947461
'''

# 3. 서울시 거주/비거주 고객의 소비액과 비율 계산
result_convi = pd.DataFrame()
result_convi['Total spent'] = convi_data.groupby('Region')['AMT'].sum()
result_convi['Spent Ratio(%)'] = ((result_convi['Total spent'] / result_convi['Total spent'].sum()) * 100).round(2)

result_region = result_convi.reset_index()

print(result_region)
'''
>>>
  Region  Total spent  Spent Ratio(%)
0    비서울  13473190145           16.84
1     서울  66513977146           83.16

ANALYSIS :
서울의 편의점 매출량이 압도적임을 알 수 있음.
소비패턴을 분석해서 매출이 높은 곳을 중점으로 마케팅 전략 수립.
'''

# 4. 거주지 소재 편의점 소비액 구하기
result_local = convi_data[convi_data['MEGA_CTY_NO'] == convi_data['CSTMR_MEGA_CTY_NO']]
result_local = pd.DataFrame({'Total spent': [result_local['AMT'].sum()]})
print(result_local)
'''
>>>
   Total spent
0  66513977146
'''