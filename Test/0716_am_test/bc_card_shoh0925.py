import pandas as pd

# 1. 파일 경로 지정
file_path = "/content/bc_card_out_2020_03.txt"

try:
    print("=== [1. 데이터 불러오기 시도] ===")

    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        df = pd.read_csv(f, sep='\t', low_memory=False)

    print("✓ 성공적으로 데이터를 불러왔습니다!")
    print("-" * 50)

    # 데이터 실제 모습 확인 (밀림 현상이 해결되었는지 확인)
    print("=== [1-1. 데이터 실제 모습 확인 (상위 3개 행)] ===")
    print(df.head(3))
    print("-" * 50)

    # -----------------------------------------
    # 2. 데이터 전처리 및 타입 변환
    # -----------------------------------------
    print("=== [2. 데이터 전처리 시작] ===")

    # 텍스트 데이터의 앞뒤 공백 제거
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # 서울시 거주자 여부 판별 (CSTMR_MEGA_CTY_NM: 고객거주 시도명)
    df['is_seoul_resident'] = df['CSTMR_MEGA_CTY_NM'] == '서울특별시'

    # 금액(AMT)과 건수(CNT) 컬럼을 안전하게 숫자형으로 변환 (혹시 모를 문자열 대비)
    df['AMT'] = pd.to_numeric(df['AMT'], errors='coerce').fillna(0)
    df['CNT'] = pd.to_numeric(df['CNT'], errors='coerce').fillna(0)

    print("✓ 전처리가 완료되었습니다.")
    print("-" * 50)

    # -----------------------------------------
    # 3. 데이터 분석
    # -----------------------------------------

    # ① 서울시 거주/비거주 고객 수 구하기
    resident_counts = df['is_seoul_resident'].value_counts()
    print("=== [3-①. 서울시 거주/비거주 고객 수] ===")
    print(f"서울 거주 고객 레코드 수: {resident_counts.get(True, 0):,}건")
    print(f"비서울 거주 고객 레코드 수: {resident_counts.get(False, 0):,}건")
    print("-" * 50)

    # ② 총 소비액 구하기
    total_amt = df['AMT'].sum()
    print("=== [3-②. 총 소비액] ===")
    print(f"전체 고객의 총 소비액: {int(total_amt):,}원")
    print("-" * 50)

    # ③ 성별 소비액 구하기
    gender_amt = df.groupby('SEX_CTGO_CD')['AMT'].sum()
    print("=== [3-③. 성별 소비액] ===")
    for sex, amt in gender_amt.items():
        if sex in ['1', 'M', 'm', '1.0']:
            sex_str = "남성"
        elif sex in ['2', 'F', 'f', '2.0']:
            sex_str = "여성"
        else:
            sex_str = f"기타/알수없음 ({sex})"
        print(f"성별 [{sex_str}]: {int(amt):,}원")
    print("-" * 50)

    # --- [편의점 소비 정보 분석] ---
    # 업종명(TP_BUZ_NM)에서 공백 제거 후 '편의점'만 필터링
    df['clean_buz_nm'] = df['TP_BUZ_NM'].str.replace(" ", "")
    convenience_df = df[df['clean_buz_nm'] == '편의점']
    convenience_total_amt = convenience_df['AMT'].sum()

    print("=== [편의점 ①. 편의점 총 소비액] ===")
    print(f"전체 편의점 소비액: {int(convenience_total_amt):,}원")
    print("-" * 50)

    # ② 강남구 편의점 소비액 분석하기 (가맹점 시군구명이 '강남구'인 곳)
    gangnam_cvs_df = df[(df['CTY_RGN_NM'] == '강남구') & (df['clean_buz_nm'] == '편의점')]
    gangnam_cvs_amt = gangnam_cvs_df['AMT'].sum()

    print("=== [편의점 ②. 강남구 편의점 소비액] ===")
    print(f"강남구 내 편의점 소비액: {int(gangnam_cvs_amt):,}원")
    print("-" * 50)

    # --- [서울시 거주/비거주 고객의 소비액 구하기] ---
    resident_amt = df.groupby('is_seoul_resident')['AMT'].sum()

    print("=== [서울시 거주/비거주 고객의 소비액] ===")
    print(f"서울 거주 고객의 총 소비액: {int(resident_amt.get(True, 0)):,}원")
    print(f"비서울 거주 고객의 총 소비액: {int(resident_amt.get(False, 0)):,}원")
    print("-" * 50)

    # --- [거주지 소재 편의점 소비액 구하기] ---
    # 고객 거주지 구(CSTMR_CTY_RGN_NM)와 가맹점 소재지 구(CTY_RGN_NM)가 일치하는 편의점 소비
    local_cvs_df = df[(df['CSTMR_CTY_RGN_NM'] == df['CTY_RGN_NM']) & (df['clean_buz_nm'] == '편의점')]
    local_cvs_amt = local_cvs_df['AMT'].sum()

    print("=== [거주지 소재 편의점 소비액] ===")
    print(f"자신이 거주하는 시군구 내 편의점에서 소비한 총 금액: {int(local_cvs_amt):,}원")
    print("-" * 50)

except Exception as e:
    print(f"⚠️ 오류 발생: {e}")