import pandas as pd

# 파일 읽기
df_card = pd.read_csv("C:/Pycharm/0716 analysis/bc_card_out2020_03.txt", sep="\t", encoding="utf-8")

# ==========================================
# 1. 원본 데이터 소개
#print(df_card.head())
#print(df_card.columns)
print(df_card.info())
print(df_card.isnull().sum())
# ==========================================
# 2. 데이터 전처리
# print("\n--- [데이터 전처리 시작] ---")

if df_card is not None:
    df = df_card.copy()

    # ① 결측치(비어있는 값) 확인 및 처리
    df = df.dropna(subset=['CSTMR_MEGA_CTY_NM', 'AMT', 'TP_BUZ_NM', 'SEX_CTGO_CD', 'CTY_RGN_NM'])

    # ② 데이터 타입 변환
    if 'AMT' in df.columns:
        df['AMT'] = pd.to_numeric(df['AMT'], errors='coerce')
        df = df.dropna(subset=['AMT'])

    # ③ 서울시 거주 여부를 판별하는 새로운 열 생성
    if 'CSTMR_MEGA_CTY_NM' in df.columns:
        df['Seoul'] = df['CSTMR_MEGA_CTY_NM'].str.contains('서울', na=False)

#    print("✓ 데이터 전처리가 완료되었습니다.")

# ==========================================
# 3. 데이터 분석
    print("\n" + "=" * 50 + "\n[서울시 거주/비거주 고객의 소비 분석]\n" + "=" * 50)

    # ① 서울시 거주/비거주 고객 수 구하기
    seoul_resident = df[df['CSTMR_MEGA_CTY_NM'] == '서울특별시']
    non_seoul_resident = df[df['CSTMR_MEGA_CTY_NM'] != '서울특별시']

    print(f"① 서울시 거주 고객 수: {len(seoul_resident):,}명")
    print(f"   서울시 비거주 고객 수: {len(non_seoul_resident):,}명")

    # ② 총 소비액 구하기
    total_seoul_amt = seoul_resident['AMT'].sum()
    total_non_seoul_amt = non_seoul_resident['AMT'].sum()

    print(f"\n② 서울시 거주 고객 총 소비액: {total_seoul_amt:,}원")
    print(f"   서울시 비거주 고객 총 소비액: {total_non_seoul_amt:,}원")

    # ③ 성별 소비액 구하기 (1: 남성, 2: 여성)
    seoul_gender_amt = seoul_resident.groupby('SEX_CTGO_CD')['AMT'].sum()
    print("\n③ 서울시 거주 고객의 성별 소비액:")
    for gender, amt in seoul_gender_amt.items():
        gender_name = "남성" if gender == 1 else "여성"
        print(f" - {gender_name}: {amt:,}원")


#  ----------------------------------------------------------------------------------

    print("\n" + "=" * 50 + "\n[편의점 소비 정보 분석]\n" + "=" * 50)

    # ① 편의점 소비액 구하기 (가맹점 업종명 '편 의 점' 필터링)
    convenience_df = df[df['TP_BUZ_NM'].str.strip() == '편 의 점']
    total_conv_amt = convenience_df['AMT'].sum()
    print(f"① 전체 편의점 총 소비액: {total_conv_amt:,}원")

    # ② 강남구 편의점 소비액 분석하기
    gangnam_conv_df = convenience_df[convenience_df['CTY_RGN_NM'] == '강남구']
    gangnam_conv_amt = gangnam_conv_df['AMT'].sum()
    print(f"② 강남구에 있는 편의점의 총 소비액: {gangnam_conv_amt:,}원")

    # ③ 서울시 거주/비거주 고객의 편의점 소비액 구하기
    conv_seoul_resident_amt = convenience_df[convenience_df['CSTMR_MEGA_CTY_NM'] == '서울특별시']['AMT'].sum()
    conv_non_seoul_resident_amt = convenience_df[convenience_df['CSTMR_MEGA_CTY_NM'] != '서울특별시']['AMT'].sum()

    print(f"\n③ 서울시 거주 고객의 편의점 소비액: {conv_seoul_resident_amt:,}원")
    print(f"   서울시 비거주 고객의 편의점 소비액: {conv_non_seoul_resident_amt:,}원")

    # ④ 거주지 소재 편의점 소비액 구하기 (자기가 사는 동네 편의점에서 쓴 금액)
    # 고객의 거주지 시군구와 가맹점 위치 시군구가 같은 조건 확인
    same_region_conv = convenience_df[convenience_df['CSTMR_CTY_RGN_NM'] == convenience_df['CTY_RGN_NM']]
    same_region_conv_amt = same_region_conv['AMT'].sum()
    print(f"\n④ 거주지 소재(본인 거주 구와 편의점 위치 일치) 편의점 소비액: {same_region_conv_amt:,}원")