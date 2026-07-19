
import pandas as pd

orig=pd.read_csv( './bc_card.txt',sep='\t', encoding='cp949',header=None)

# 0. 표 고치기 ===========================================
values = orig.iloc[0].tolist()
print(orig.shape) #(1, 2200045), 지금부터 이친구를 제대로된 표로 만들겠습니다
print(values[20:25]) #['FLC', 'AMT', 'CNT201906', np.int64(11), '서울특별시'] < CNT 컬럼 이후 줄바꿈이 안된 상태

columns=values[:22]+['CNT'] #컬럼에 CNT 다시 추가

rows=[]
for i in range(22,len(values)-1,22):
    reg=str(values[i])[-6:]
    row=[reg]+values[i+1:i+22]

    if i+22 == len(values) -1:
        cnt=values[-1]
    else:
        cnt=str(values[i+22])[:6]

    row.append(cnt)
    rows.append(row)


df= pd.DataFrame(rows,columns=columns)

# 1. 원본 데이터 소개 =========================================

print('행,열:', df.shape) # 행과 열 개수 (100001, 23)
print('---------------데이터 확인 시작---------------')
print('\n')
print('-head-')
print(df.head()) # 상위 n개 데이터
'''
  REG_YYMM  MEGA_CTY_NO     MEGA_CTY_NM  CTY_RGN_NO ...   AGE_VAL  FLC    AMT     CNT
0   201906           11       서울특별시        1162  ...     30대    2  26284804  189220
1   201906           11       서울특별시        1159  ...     20대    1    109290  182019
2   201906           11       서울특별시        1162  ...     20대    1    268850  522019
3   201906           11       서울특별시        1144  ...     20대    1  44174450  179020
4   201906           11       서울특별시        1120  ...     20대    1  60338146  353620
'''
print('\n')
print('-info-')
print(df.info())
'''
 #   Column             Non-Null Count   Dtype 
---  ------             --------------   ----- 
 0   REG_YYMM           100001 non-null  str   
 1   MEGA_CTY_NO        100001 non-null  int64 
 2   MEGA_CTY_NM        100001 non-null  str   
 3   CTY_RGN_NO         100001 non-null  int64 
 4   CTY_RGN_NM         100001 non-null  str   
 5   ADMI_CTY_NO        100001 non-null  int64 
 6   ADMI_CTY_NM        100001 non-null  str   
 7   MAIN_BUZ_CODE      100001 non-null  int64 
 8   MAIN_BUZ_DESC      100001 non-null  str   
 9   TP_GRP_NO          100001 non-null  int64 
 10  TP_GRP_NM          100001 non-null  str   
 11  TP_BUZ_NO          100001 non-null  int64 
 12  TP_BUZ_NM          100001 non-null  str   
 13  CSTMR_GUBUN        100001 non-null  str   
 14  CSTMR_MEGA_CTY_NO  100001 non-null  int64 
 15  CSTMR_MEGA_CTY_NM  100001 non-null  str   
 16  CSTMR_CTY_RGN_NO   100001 non-null  int64 
 17  CSTMR_CTY_RGN_NM   100001 non-null  str   
 18  SEX_CTGO_CD        100001 non-null  int64 
 19  AGE_VAL            100001 non-null  str   
 20  FLC                100001 non-null  int64 
 21  AMT                100001 non-null  int64 
 22  CNT                100001 non-null  object
'''
print('\n')
print('-describe-')
print(df.describe())
'''
       MEGA_CTY_NO     CTY_RGN_NO  ...            FLC           AMT
count     100001.0  100001.000000  ...  100001.000000  1.000010e+05
mean          11.0    1144.198688  ...       2.650293  2.662476e+06
std            0.0      20.755590  ...       1.353630  1.547484e+07
min           11.0    1111.000000  ...       1.000000  3.000000e+02
25%           11.0    1123.000000  ...       1.000000  8.890000e+04
50%           11.0    1147.000000  ...       2.000000  2.509000e+05
75%           11.0    1165.000000  ...       4.000000  9.178000e+05
max           11.0    1174.000000  ...       5.000000  1.017956e+09
'''
print('---------------데이터 확인 종료---------------')
# 2. 데이터 전처리 ===========================================
## 결측치 없음
print('\n')
print('---------------데이터 전처리 시작---------------')
print('\n')
print('중복 행 개수:', df.duplicated().sum()) #중복 행 개수: 0

# 필요한 정보 :  시도명 , 시군구명, 거주지 시도명, 거주지 시군구명, , 업종 소분류명, 성별, 이용 금액
card_data = df[['MEGA_CTY_NM','CTY_RGN_NM','CSTMR_MEGA_CTY_NM','CSTMR_CTY_RGN_NM','TP_BUZ_NM','SEX_CTGO_CD','AMT']]
card_data = card_data.rename(columns={'MEGA_CTY_NM': '시군구명','CTY_RGN_NM': '시도명','CSTMR_MEGA_CTY_NM': '거주지 시도명','CSTMR_CTY_RGN_NM': '거주지 시군구명','TP_BUZ_NM': '업종 소분류명','SEX_CTGO_CD': '성별','AMT': '이용 금액'})

print('\n')
print('Column:',card_data.columns)
#Index(['시군구명', '시도명', '거주지 시도명', '거주지 시군구명','업종 소분류명' '성별', '이용 금액'], dtype='str')
print('\n')
print('-info-')
print(card_data.info())
'''
 #   Column    Non-Null Count   Dtype
---  ------    --------------   -----
 0   시군구명      100001 non-null  str  
 1   시도명       100001 non-null  str  
 2   거주지 시도명   100001 non-null  str  
 3   거주지 시군구명  100001 non-null  str  
 4   업종 소분류명   100001 non-null  str  
 5   성별        100001 non-null  int64
 6   이용 금액     100001 non-null  int64
'''
print('\n')
print('-head-')
print(card_data.head(5))
'''
    시군구명  시도명 거주지 시도명 거주지 시군구명 업종 소분류명  성별     이용 금액
0  서울특별시  관악구   서울특별시      관악구    서양음식   2  26284804
1  서울특별시  동작구   서울특별시      서초구   편 의 점   2    109290
2  서울특별시  관악구   서울특별시      관악구  기타음료식품   1    268850
3  서울특별시  마포구   서울특별시      은평구    일반한식   1  44174450
4  서울특별시  성동구   서울특별시      성동구    일반한식   1  60338146

'''
print('행,열:', card_data.shape) #(100001, 7)
print('\n')
print('---------------데이터 전처리 종료---------------')
# 3. 데이터 분석 ===========================================
print('\n')
## 서울시 거주 / 비거주 고객의 소비 분석 -----------------------------
print('---------------데이터 분석 시작---------------')
### 1) 서울시 거주/비거주 고객 수 구하기
cstmr_seoul = card_data[card_data['거주지 시도명']=='서울특별시']
cstmr_notseoul = card_data[card_data['거주지 시도명']!='서울특별시']

print('\n')
print('-서울시 거주/비거주 고객 수-')
print(f'서울시민: {len(cstmr_seoul)}명')
print(f'그 외 시민: {len(cstmr_notseoul)}명')

### 2) 총 소비액 구하기
all_amount=card_data['이용 금액'].sum()
print('\n')
print(f'총 소비액: {all_amount}') #총 소비액: 266250278498

### 3) 성별 소비액 구하기
gen_data=card_data.groupby('성별')['이용 금액'].sum()
print(f'여성 소비액 : {gen_data[2]} / 남성 소비액 : {gen_data[1]}')

## 편의점 소비 정보 분석 ------------------------------------------

### 1) 편의점 소비액 구하기
com_data=card_data[card_data['업종 소분류명'] == '편 의 점']
print(com_data['이용 금액'].sum())

### 2) 강남구 편의점 소비액 구하기
Gcom_data=com_data[com_data['시군구명'] == '강남구']
com_sum = com_data['이용 금액'].sum()
print('편의점 소비액:', com_sum)


## 서울시 거주 / 비거주 고객의 소비액 구하기 -----------------------------
print(f'서울시민 소비액: {cstmr_seoul['이용 금액'].sum()}')
print(f'그 외 시민 소비액: {cstmr_notseoul['이용 금액'].sum()}')



## 거주지 소재 편의점 소비액 구하기 -------------------------------------
com_datagroup=com_data.groupby('거주지 시도명')['이용 금액'].sum()
print('\n')
print('-거주지 소재별 편의점 소비액-')
print(com_datagroup)
print('---------------데이터 분석 종료---------------')


