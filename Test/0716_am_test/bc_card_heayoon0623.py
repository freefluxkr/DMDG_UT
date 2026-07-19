import pandas as pd

# 파일경로 지정
file_path = r"/content/bc_card_out2020_03.txt"

# with 문으로 파일 객체를 안전하게 오픈
try :
    with open(file_path, "r", encoding='utf-8') as f:
        df = pd.read_csv(f, sep='\t', low_memory=False)
    print("성공적으로 데이터를 불러왔습니다.")
    print(df.head())
except Exception as e:
    print(f"오류발생: {e}")

#1. 컬럼 이름 뭐 필요한지 데이터 프레임으로 묶기

df_name = df[[
    'CSTMR_MEGA_CTY_NM',  # 고객 거주지 시도(서울, 경기도 등등)
    'MEGA_CTY_NM',       # 카드를 긁은 가맹점 시-도
    'CTY_RGN_NM',        # 카드를 긁은 가맹점 구(강남구, 성북구 등등)
    'TP_BUZ_NM',         # 가맹점 업종(편 의 점)
    'SEX_CTGO_CD',       # 고객 성별(1: 남, 2: 여)
    'AMT'                # 카드결제금액(소비액)
]].copy()

#2. 묶은거 한글로 바꾸기

df_name = df_name.rename(columns = {
    'CSTMR_MEGA_CTY_NM' : '고객시도',
    'MEGA_CTY_NM': '가맹점시도',
    'CTY_RGN_NM': '가맹점소재지구',
    'TP_BUZ_NM': '업종소분류코드',
    'SEX_CTGO_CD': '성별',
    'AMT': '이용금액'
})


#3. 파생변수 제작1) 서울 거주자 여부 구분하기
# 고객거주지('고객시도')가 서울이면 '서울거주', 아니면 '비서울거주'
df_name['거주구분'] = '비서울거주' 
df_name.loc[df_name['고객시도'] == '서울특별시' , '거주구분'] = '서울거주' #서울 거주하는 사람만 바꿔주기.

# 문제1번

import pandas as pd

print(f"서울 거주 총 인구 : {df_name[df_name['거주구분'] == '서울거주'].shape[0] :,d}명")
#서울에 거주하는 남성
print(f"  - 서울시 거주 남성 : {df_name[(df_name['거주구분'] == '서울거주') & (df_name['성별'] == 1)].shape[0]:,d}명")
#서울에 거주하는 여성
print(f"  - 서울시 거주 여성 : {df_name[(df_name['거주구분'] == '서울거주') & (df_name['성별'] == 2)].shape[0]:,d}명")
#서울에 거주하지 않는 총 인구
print(f"\n 비서울 거주 총 인구 : {df_name[df_name['거주구분'] == '비서울거주'].shape[0] :,d}명")
#서울에 거주하지 않는 남성
print(f"  - 비서울 거주 남성 : {df_name[(df_name['거주구분'] == '비서울거주') & (df_name['성별'] == 1)].shape[0]:,d}명")
#서울에 거주하지 않는 여성
print(f"  - 비서울 거주 여성 : {df_name[(df_name['거주구분'] == '비서울거주') & (df_name['성별'] == 2)].shape[0]:,d}명")

#문제2번

# 서울거주 vs 비서울거주 고객 소비 분석
# 서울거주/비서울거주 총 소비액 구하기
overall_spend = df_name.groupby('거주구분')['이용금액'].sum()
print("거주 구분별 총 소비액  ")
print(f"  - 서울 거주자 총 소비액 :  {overall_spend.get('서울거주', 0):,d} 원")
print(f"  - 비서울 거주자 총 소비액 :  {overall_spend.get('비서울거주', 0):,d} 원")

#문제3번

# 서울거주/비서울거주 성별 소비액 구하기
gender_spend = df_name.groupby(['거주구분', '성별'])['이용금액'].sum()
print("\n 거주 구분 내 성별 소비액 : ")
print(f" - [서울 거주] 남성 소비액 : {gender_spend.get(('서울거주', 1), 0):,d} 원")
print(f" - [서울 거주] 여성 소비액 : {gender_spend.get(('서울거주', 2), 0):,d} 원")
print("비서울 부분")
print(f" - [비서울 거주] 남성 소비액 : {gender_spend.get(('비서울거주', 1), 0):,d} 원")
print(f"  -[비서울 거주] 여성 소비액 : {gender_spend.get(('비서울거주', 2), 0) :,d} 원")



# 편의점 소비액 구하기
df_name['업종_공백제거'] = df_name['업종소분류코드'].str.replace(' ', '')
df_cvs = df_name[df_name['업종_공백제거'] == '편의점'].copy()

# 편의점 총 소비액
total_cvs_spend = df_cvs['이용금액'].sum()
print(f"편의점 총 소비액 : {total_cvs_spend:,d} 원")

# 강남구 편의점 소비액
gangnam_cvs_spend = df_cvs[df_cvs['가맹점소재지구'] == '강남구']['이용금액'].sum()
print(f"강남구 편의점 총 소비액 : {gangnam_cvs_spend:,d} 원")

# 서울시 거주 편의점 소비액
df_cvs_seoul = df_cvs[df_cvs['거주구분'] == '서울거주'].copy()
total_cvs_spend_seoul = df_cvs_seoul['이용금액'].sum()
print(f"서울시 거주 편의점 총 소비액 : {total_cvs_spend_seoul:,d} 원")
# 비서울 거주 편의점 소비액
df_cvs_notsoeul = df_cvs[df_cvs['거주구분'] == '비서울거주'].copy()
total_cvs_spend_notsoeul = df_cvs_notsoeul['이용금액'].sum()
print(f"비서울 거주 편의점 총 소비액 : {total_cvs_spend_notsoeul:,d} 원")





