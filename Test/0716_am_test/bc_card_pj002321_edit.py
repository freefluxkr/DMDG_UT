# Last updated: 2026-07-16
# last update : 2026-07-16
import os
import pandas as pd
import csv
from pathlib import Path
'''
 1. 원본 데이터 소개
 2. 데이터 전처리
 3. 서울시 거주/비거주 고객의 소비 분석 (고객 수 / 총 소비액 / 성별 소비액)
 4. 편의점 소비 정보 분석 (소비액 / 강남구 / 거주·비거주 / 거주지 소재)
'''
ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Asset")


# ====================== 데이터 읽기/전처리 ======================
def load_data(file_name):
    path = os.path.join(ASSET_DIR,file_name)
    return pd.read_csv(path,sep="\t",encoding="utf-8")

def load_broken_data(file_name):
    """줄바꿈이 사라진 파일(bc_card_output.txt) 복구용.
    모든 값이 탭으로만 이어져 있어 read_csv가 1행으로 읽어버린다.
    -> 탭으로 나눈 뒤 23칸(컬럼 수)씩 잘라 행을 되살린다.
    행 경계에는 'CNT값+다음 행 연월'이 붙어 있어서(예: '1892201906'
    = CNT 1892 + REG_YYMM 201906) 뒤 6자리를 떼어 다음 행 시작으로 쓴다."""
    path = os.path.join(ASSET_DIR, file_name)
    file = open(path, "r", encoding="utf-8")
    tokens = file.read().split("\t")
    file.close()

    rows = []
    row = []
    for token in tokens[0:-1]:        # 맨 마지막 값 하나만 빼고 순서대로 처리
        if len(row) < 22:             # 한 행(23칸)이 아직 안 찼으면 그대로 추가
            row.append(token)
        else:                         # 23번째 칸 = 'CNT값+다음 행 연월' 덩어리
            row.append(token[0:-6])
            rows.append(row)
            row = [token[-6:]]
    row.append(tokens[-1])            # 파일 맨 마지막 값은 CNT만 있음
    rows.append(row)

    df = pd.DataFrame(rows[1:], columns=rows[0])   # rows[0] = 컬럼 이름 행
    # 복구 과정에서 전부 문자열이 됐으므로 분석에 쓰는 숫자 컬럼만 int로 변환
    for col in ["CTY_RGN_NO", "TP_BUZ_NO", "CSTMR_MEGA_CTY_NO",
                "CSTMR_CTY_RGN_NO", "SEX_CTGO_CD", "AMT", "CNT"]:
        df[col] = df[col].apply(int)
    return df

def divide_resident(code):
    # CSTMR_MEGA_CTY_NO 11(서울특별시) -> 서울 거주 / 그 외(부산26, 인천28, 경기41 등) -> 서울 비거주
    if code == 11:
        return "서울 거주"
    return "서울 비거주"
    
def divide_gender(code):
    # SEX_CTGO_CD 1-> male, 2->female
    if code ==1 :
        return "남성"
    return "여성"

def preprocess(df):
    # 분석에 쓸 파생 칼럼 2개 추가
    df["거주구분"] = df["CSTMR_MEGA_CTY_NO"].apply(divide_resident)
    df["성별"] = df["SEX_CTGO_CD"].apply(divide_gender)
    return df

def number_fomatting(number):
    # 숫자 출력용 1,234
    return f"{number:,}"

def format_table(table):
    # 피벗 테이블의 모든 컬럼 숫자를 1,234 형태로 변환
    for col in table.columns:
        table[col] = table[col].apply(number_fomatting)
    return table

# ====================== 분석 절차 ======================
def info(label,df):
    # 1. 원본 데이터 소개
    print(f"\n[{label}] {len(df):,}행 x {len(df.columns)}컬럼")
    print("컬럼:",list(df.columns))
    print(df.head(3).to_string(index=False))

def check_preprocess(label,df):
    # 2. 전처리 확인 (결측치, 파생 컬럼 분포)
    print(f"\n[{label}] 결측치 합계 : {df.isnull().sum().sum()}개")
    print(df["거주구분"].value_counts().to_string())

def resident_count(label,df):
    # 3-1 거주/비거주 고객 수 (집계 데이터라 CNT = 카드 이용 건수 합으로 계산)
    print(f"\n[{label}]")
    print(df.groupby("거주구분")["CNT"].sum().apply(number_fomatting).to_string(),"건")

def resident_amount(label,df):
    # 3-2/4-3 거주/비거주 소비액
    print(f"\n[{label}]")
    print(df.groupby("거주구분")["AMT"].sum().apply(number_fomatting).to_string(),"원")

def resident_gender_amount(label,df):
    # 3-3 거주/비거주 성별 소비액
    print(f"\n[{label}]")
    table = df.pivot_table(index="거주구분",columns="성별",values="AMT",aggfunc="sum")
    print(format_table(table))

def cvs_amount(label,df,cvs):
    # 4-1 편의점 소비액 (전체 대비 비중 + 자치구 상위5)
    total = cvs["AMT"].sum()
    ratio = round(total / df["AMT"].sum()*100,1)
    print(f"\n[{label}] 편의점 소비액 : {number_fomatting(total)}원 (전체의 {ratio}%)")
    gu = cvs.groupby("CTY_RGN_NM")["AMT"].sum()
    print(gu.sort_values(ascending=False).head(5).apply(number_fomatting).to_string()+"원")

def gangnam_cvs(label,cvs):
    # 4-2 강남구 편의점 소비액 분석 (연령대 x 성별)
    gangnam = cvs[cvs["CTY_RGN_NM"]=="강남구"]
    print(f"[{label}] 강남구 편의점 소비액 : {number_fomatting(gangnam['AMT'].sum())}")
    table = gangnam.pivot_table(index="AGE_VAL",columns="성별",values="AMT",aggfunc="sum")
    print(format_table(table))

def home_cvs_amount(label,cvs):
    # 4-4 거주지 소재 편의점 소비액
    # 서울 거주 고객 중 매장 자치구(CTY_RGN_NO) == 거주 자치구(CSTMR_CTY_RGN_NO)
    seoul = cvs[cvs["거주구분"] == "서울 거주"]
    home = seoul[seoul["CTY_RGN_NO"] == seoul["CSTMR_CTY_RGN_NO"]]
    away = seoul[seoul["CTY_RGN_NO"] != seoul["CSTMR_CTY_RGN_NO"]]
    print(f"\n[{label}] 거주 자치구 편의점: {number_fomatting(home['AMT'].sum())}원"
          f" / 다른 자치구 편의점: {number_fomatting(away['AMT'].sum())}원")


# ================================== 실행 ========================================
df_2019 = preprocess(load_broken_data("../data/bc_card_output.txt"))
df_2020 = preprocess(load_data("../data/bc_card_out2020_03.txt"))
datasets = [("2019년 6월", df_2019), ("2020년 3월", df_2020)]

# 편의점(TP_BUZ_NO 4010(업종코드) = '편 의 점')은 STEP 4에서 계속 쓰므로 미리 필터링
cvs_2019 = df_2019[df_2019["TP_BUZ_NO"] == 4010]
cvs_2020 = df_2020[df_2020["TP_BUZ_NO"] == 4010]
cvs_datasets = [("2019년 6월", cvs_2019), ("2020년 3월", cvs_2020)]

print("="*60, "1. 원본 데이터 소개")
for label,df in datasets:
    info(label,df)

print("="*60, "2. 데이터 전처리 (거주구분/성별 컬럼 추가)")
for label, df in datasets:
    check_preprocess(label,df)


print("="*60, "3-1. 서울시 거주/비거주 고객 수(이용 건수)")
for label, df in datasets:
    resident_count(label,df)


print("="*60, "3-2. 서울시 거주/비거주 총 소비액")
for label, df in datasets:
    resident_amount(label,df)


print("="*60, "3-3. 서울시 거주/비거주 성별 소비액")
for label, df in datasets:
    resident_gender_amount(label,df)


print("=" * 60, "\n4-1. 편의점 소비액")
cvs_amount("2019년 6월", df_2019, cvs_2019)
cvs_amount("2020년 3월", df_2020, cvs_2020)

print("=" * 60, "\4-2. 강남구 편의점 소비액 분석")
for label, cvs in cvs_datasets:
    gangnam_cvs(label, cvs)

print("=" * 60, "\n4-3. 편의점의 거주/비거주 고객 소비액")
for label, cvs in cvs_datasets:
    resident_amount(label, cvs)

print("=" * 60, "\n4-4. 거주지 소재 편의점 소비액(동네 안/밖)")
for label, cvs in cvs_datasets:
    home_cvs_amount(label, cvs)