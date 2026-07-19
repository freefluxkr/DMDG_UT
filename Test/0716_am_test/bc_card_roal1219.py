import pandas as pd

bc_card_out2020 = pd.read_csv('bc_card_out2020_03.txt',sep='\t', encoding='utf-8')
print(bc_card_out2020.head(5))
'''
0    202003           11       서울특별시        1168  ...     20대    1   7927440  1089
1    202003           11       서울특별시        1129  ...     40대    4    274100    25
2    202003           11       서울특별시        1144  ...  60대 이상    5  34395725   808
3    202003           11       서울특별시        1126  ...     20대    1  31860800  3699
4    202003           11       서울특별시        1168  ...     50대    4   2546487    45

'''
#file_bc_Card = r"C:\work\0716\bc_card.txt"

#with open(file_bc_Card,'r',encoding='cp949') as f1:
#    bc_card = pd.read_csv(f1,sep='\t', low_memory=False)
#    print(bc_card.head())

# 지울 컬럼명 리스트
columns_to_del = [
    'REG_YYMM', 'MEGA_CTY_NO', 'MEGA_CTY_NM', 'CTY_RGN_NO',
    'ADMI_CTY_NO', 'ADMI_CTY_NM', 'MAIN_BUZ_CODE', 'MAIN_BUZ_DESC',
    'TP_GRP_NO', 'TP_GRP_NM', 'TP_BUZ_NO', 'CSTMR_GUBUN',
    'CSTMR_MEGA_CTY_NO', 'CSTMR_CTY_RGN_NO', 'AGE_VAL', 'FLC', 'CNT']

# del 명령어로 하나씩 지우기
for col in columns_to_del:
    del bc_card_out2020[col]

# 결과 확인
print(bc_card_out2020.head())
'''
  CTY_RGN_NM TP_BUZ_NM  ... SEX_CTGO_CD       AMT
0        강남구     편 의 점  ...           2   7927440
1        성북구        약국  ...           1    274100
2        마포구   인터넷 P/G  ...           1  34395725
3        중랑구     편 의 점  ...           2  31860800
4        강남구     생명 보험  ...           2   2546487

'''

#결측치 확인
print(bc_card_out2020.info())
print(bc_card_out2020.isnull().sum())

'''
dtypes: int64(2), str(4)
memory usage: 72.8 MB
None
CTY_RGN_NM           0
TP_BUZ_NM            0
CSTMR_MEGA_CTY_NM    0
CSTMR_CTY_RGN_NM     0
SEX_CTGO_CD          0
AMT                  0
dtype: int64
'''

# 서울시 거주/비거주 고객 수 구하기
seoul_cust = bc_card_out2020[bc_card_out2020['CSTMR_MEGA_CTY_NM'] == '서울특별시']
non_seoul_cust = bc_card_out2020[bc_card_out2020['CSTMR_MEGA_CTY_NM'] != '서울특별시']

print(f"서울시 거주 고객 수 : {len(seoul_cust):,}명")
print(f"서울시 비거주 고객 수: {len(non_seoul_cust):,}명\n")

'''
서울시 거주 고객 수 : 901,072명
서울시 비거주 고객 수: 688,422명

'''
# 총 소비액 구하기
bc_card_amt = pd.to_numeric(bc_card_out2020['AMT'])
all_cost = bc_card_amt.sum()
print(f"총 소비액 : {all_cost:,.0f}원\n")

'''
총 소비액 : 3,326,813,919,531원
'''

# 성별간 소비액

gender_cost = seoul_cust.groupby('SEX_CTGO_CD')['AMT'].sum()
print(" 서울특별시 성별별 소비액:")
for gender, cost in gender_cost.items():
    if gender == 1:
        print(f" 남성 : {cost:,.0f}원")
    else :
        print(f" 여성 : {cost:,.0f}원")
'''
성별별 소비액:
 남성 : 1,698,104,408,917원
 여성 : 1,628,709,510,614원
'''

# 편의점 소비액
convenience = bc_card_out2020[bc_card_out2020['TP_BUZ_NM'] == '편 의 점']
convenience_total_amt = convenience['AMT'].sum()
print(f"편의점 총 소비액 : {convenience_total_amt:,.0f}원\n")

'''
편의점 총 소비액 : 79,987,167,291원
'''

#강남구 소비액
gangnam_conv = convenience[convenience['CTY_RGN_NM'] == '강남구']
gangnam_conv_amt = gangnam_conv['AMT'].sum()
print(f"강남구 편의점 소비액 : {gangnam_conv_amt:,.0f}원\n")

#서울시 거주/비거주 소비액
seoul_conv_amt = convenience[convenience['CSTMR_MEGA_CTY_NM'] == '서울특별시']['AMT'].sum()
non_seoul_conv_amt = convenience[convenience['CSTMR_MEGA_CTY_NM'] != '서울특별시']['AMT'].sum()

'''
강남구 편의점 소비액 : 8,170,947,461원
'''

print(f"서울시 거주 고객의 편의점 소비액 : {seoul_conv_amt:,.0f}원")
print(f"서울시 비거주 고객의 편의점 소비액 : {non_seoul_conv_amt:,.0f}원\n")

'''
서울시 거주 고객의 편의점 소비액 : 66,513,977,146원
서울시 비거주 고객의 편의점 소비액 : 13,473,190,145원
'''

#거주지 소재 편의점 소비액 구하기
cheongju_conv = convenience[convenience['CTY_RGN_NM'] == '청주시']
cheongju_conv_amt = gangnam_conv['AMT'].sum()
print(f"청주시 편의점 소비액 : {cheongju_conv_amt:,.0f}원\n")

'''
청주시 편의점 소비액 : 8,170,947,461원
'''

