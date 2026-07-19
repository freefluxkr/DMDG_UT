import pandas as pd

df = pd.read_csv(r'C:\Users\최우진\Downloads\bc_card_out2020_03.txt', encoding='utf-8', sep='\t')

# print(df.info())
# print(df.head(50))# 1. 원본데이터 소개 BC카드 고객 소비내역을 확인할 수가 있습니다
# print(df.isnull().sum())
df = df.dropna()
df = df.drop_duplicates() # 2. 데이터 전처리과정
df = df[df['AMT'] > 0]
df = df[df['CNT'] > 0]

in_seoul = df[df['CSTMR_MEGA_CTY_NM'] == '서울특별시']
out_seoul = df[df['CSTMR_MEGA_CTY_NM'] != '서울특별시']
print('서울거주고객 수 : ', len(in_seoul), '명')
print('서울비거주고객 수 : ', len(out_seoul), '명') # 서울거주 비거주 고객 수 체크
##### bc_card 데이터 전체 소비액 구하기
print(f"총 소비액 {df['AMT'].sum():,}원") # 총 소비액 구하기 금액 3326813919531원

male = df[df['SEX_CTGO_CD'] == 1]
female = df[df['SEX_CTGO_CD'] == 2]
male_spending = male['AMT'].sum()
female_spending = female['AMT'].sum()
print(f'남자소비 {male_spending:,}원') # 남자 소비액 확인
print(f'여자소비 {female_spending:,}원') # 여자 소비액 확인
######## 편의점 소비 정보 분석
conbini = df[df['TP_BUZ_NM'] == '편 의 점']
conbini_total_spend = conbini['AMT'].sum()
print(f'편의점 총소비액 : {conbini_total_spend:,}') # 편의점 소비액 구하기

####### 강남구 편의점 소비액
gangnam = df[df['CTY_RGN_NM'] == '강남구']
gang_conbini_spend = gangnam.groupby(df['TP_BUZ_NM'])['AMT'].sum()
print(f'강남구 편의점 소비액{gang_conbini_spend['편 의 점']:,}원') # 강남구 편의점 소비액 구하기

Y_seoul = df[df['CSTMR_MEGA_CTY_NM'] == '서울특별시']
N_seoul = df[df['CSTMR_MEGA_CTY_NM'] != '서울특별시']
print(f"서울거주 소비총합 {Y_seoul['AMT'].sum():,}원") # 서울거주 비거주 고객 소비액 총합구하기
print(f"서울비거주 소비총합 {N_seoul['AMT'].sum():,}원") # 서울거주 비거주 고객 소비액 총합구하기

####### 구로3동 거주지로 가정, 거주지 편의점 소비액 구하기
Guro3 = df[df['ADMI_CTY_NM'] == '구로3동']
Guro3_conbini = Guro3.groupby(['TP_BUZ_NM'])['AMT'].sum()
print(f'구로3동 편의점 소비액 {Guro3_conbini['편 의 점']:,}원') # 구로3동 거주지 편의점 소비액
