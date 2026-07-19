import pandas as pd

# 1. 23개의 컬럼 정의
def read_csv(file_path):
    columns = [
        'REG_YYMM', 'MEGA_CTY_NO', 'MEGA_CTY_NM', 'CTY_RGN_NO', 'CTY_RGN_NM', 
        'ADMI_CTY_NO', 'ADMI_CTY_NM', 'MAIN_BUZ_CODE', 'MAIN_BUZ_DESC', 
        'TP_GRP_NO', 'TP_GRP_NM', 'TP_BUZ_NO', 'TP_BUZ_NM', 'CSTMR_GUBUN', 
        'CSTMR_MEGA_CTY_NO', 'CSTMR_MEGA_CTY_NM', 'CSTMR_CTY_RGN_NO', 
        'CSTMR_CTY_RGN_NM', 'SEX_CTGO_CD', 'AGE_VAL', 'FLC', 'AMT', 'CNT'
    ]
    
    # 2. 파일 읽기 및 공백 기준 쪼개기
    with open(file_path, 'r', encoding='cp949') as f:
        raw_data = f.read()
    
    tokens = raw_data.split('\t')
    
    # 3. 헤더(23개) 제외하고 실제 데이터만 추출
    data_tokens = tokens[23:]
    
    # 4. 붙어 있는 CNT와 REG_YYMM을 떼어내며 행(Row) 재구성
    rows = []
    current_row = []
    
    # 첫 번째 행의 REG_YYMM은 파일 처음에 정상적으로 분리되어 있으므로 수동으로 넣어줍니다.
    if data_tokens:
        current_row.append(data_tokens[0])
    
    # 두 번째 토큰부터 돌면서 데이터 재배치
    for token in data_tokens[1:]:
        # 한 행에 22개 컬럼이 찼고, 이제 마지막 23번째 데이터(CNT와 다음 REG_YYMM이 붙은 토큰)를 처리할 차례인 경우
        if len(current_row) == 22:
            # 뒤의 6자리는 다음 행의 REG_YYMM, 그 앞은 현재 행의 CNT
            cnt_val = token[:-6]
            next_reg_yymm = token[-6:]
            
            current_row.append(cnt_val)  # 현재 행 완성 (23개)
            rows.append(current_row)     # 완료된 행 추가
            
            # 새 행을 시작하며 떼어낸 다음 REG_YYMM을 첫 값으로 지정
            current_row = [next_reg_yymm]
        else:
            current_row.append(token)
    
    # 마지막 행에 남아있는 데이터가 있다면 CNT 값을 그대로 넣어 마무리
    if len(current_row) == 23:
        rows.append(current_row)
    elif len(current_row) == 22:
        # 마지막 값에 다음 REG_YYMM이 붙어있지 않으므로 통째로 CNT로 인정
        rows.append(current_row)
    
    # 5. 데이터프레임 생성
    df = pd.DataFrame(rows, columns=columns)    
    
    df['AMT'] = pd.to_numeric(df['AMT'])
    
    return df

def analysis(df):
    df['서울거주여부'] = df['CSTMR_MEGA_CTY_NM'].apply(lambda x: '거주' if '서울' in str(x) else '비거주')
    resident_counts = df['서울거주여부'].value_counts()
    residentinseoul_sum = df.groupby('서울거주여부')['AMT'].sum()
    gender_amt_sum = df.groupby(['서울거주여부','SEX_CTGO_CD'])['AMT'].sum()

    cs = df[df['TP_BUZ_NM']=="편 의 점"]
    gangnamcs = cs[cs['CSTMR_CTY_RGN_NM']=="강남구"]

    cs_residentinseoul_sum = cs.groupby('서울거주여부')['AMT'].sum()
    cs_location_sum = cs.groupby(['CSTMR_CTY_RGN_NM'])['AMT'].sum()
    print(f"=== {df.shape} ===")
    print("서울거주여부 카운트:", resident_counts)
    print("서울거주여부별 소비합:", residentinseoul_sum)
    print("성별 소비합:", gender_amt_sum)
    if not cs.empty:
        print("편의점 소비합:", cs['AMT'].sum())
        print("강남구 편의점 소비합:", gangnamcs['AMT'].sum())
        print("편의점 서울거주여부별 소비합:", cs_residentinseoul_sum)
        print("편의점 거주지역별 소비합:", cs_location_sum)


df_out = read_csv('../data/bc_card_out2020_03.txt')
df_output = read_csv('../data/bc_card_output.txt')
df_card = read_csv('../data/bc_card.txt')

analysis(df_out)
analysis(df_output)
analysis(df_card)


"""
df_card['서울거주여부'] = df_card['CSTMR_MEGA_CTY_NM'].apply(lambda x: '거주' if '서울' in str(x) else '비거주')
resident_counts = df_card['서울거주여부'].value_counts()
residentinseoul_sum = df_card.groupby('서울거주여부')['AMT'].sum()
gender_amt_sum = df_card.groupby(['서울거주여부','SEX_CTGO_CD'])['AMT'].sum()

cs = df_card[df_card['TP_BUZ_NM']=="편 의 점"]
gangnamcs = cs[cs['CSTMR_CTY_RGN_NM']=="강남구"]

cs_residentinseoul_sum = cs.groupby('서울거주여부')['AMT'].sum()
cs_location_sum = cs.groupby(['CSTMR_CTY_RGN_NM'])['AMT'].sum()
    print(f"=== {df.shape} ===")
    print("서울거주여부 카운트:", resident_counts)
    print("서울거주여부별 소비합:", residentinseoul_sum)
    print("성별 소비합:", gender_amt_sum)
    if not cs.empty:
        print("편의점 소비합:", cs['AMT'].sum())
        print("강남구 편의점 소비합:", gangnamcs['AMT'].sum())
        print("편의점 서울거주여부별 소비합:", cs_residentinseoul_sum)
        print("편의점 거주지역별 소비합:", cs_location_sum)

"""

