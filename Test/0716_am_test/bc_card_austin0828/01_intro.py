# -*- coding: utf-8 -*-
"""
01. 원본 데이터 소개
--------------------
BC카드 소비 데이터 3종 파일의 원본 상태(크기, 인코딩, 줄바꿈, 컬럼 구조)를 확인한다.

파일 구성
  - bc_card.txt              : 2019년 6월, 서울 지역 카드소비 데이터 (CP949 인코딩, 개행문자 없음)
  - bc_card_output (1).txt   : bc_card.txt와 동일한 데이터를 UTF-8로 재인코딩한 사본 (개행문자 없음)
  - bc_card_out2020_03.txt   : 2020년 3월, 전국 카드소비 데이터 (UTF-8, 정상 개행)
"""
import os
import pandas as pd

pd.set_option("display.max_columns", None) # 컬럼 생략 없이 모든 컬럼 출력
pd.set_option("display.width", 160) # 터미널에서 한줄에 160자 출력

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {
    "bc_card.txt": "cp949",
    "bc_card_output (1).txt": "utf-8",
    "bc_card_out2020_03.txt": "utf-8",
}

# 컬럼 설명 (BC카드 지역별 업종별 소비 데이터 공통 스키마) (딕셔너리)
COLUMN_DESC = {
    "REG_YYMM": "기준연월",
    "MEGA_CTY_NO": "가맹점 광역시도 코드",
    "MEGA_CTY_NM": "가맹점 광역시도명",
    "CTY_RGN_NO": "가맹점 시군구 코드",
    "CTY_RGN_NM": "가맹점 시군구명",
    "ADMI_CTY_NO": "가맹점 행정동 코드",
    "ADMI_CTY_NM": "가맹점 행정동명",
    "MAIN_BUZ_CODE": "업종 대분류 코드",
    "MAIN_BUZ_DESC": "업종 대분류명",
    "TP_GRP_NO": "업종 그룹 코드",
    "TP_GRP_NM": "업종 그룹명",
    "TP_BUZ_NO": "세부 업종 코드",
    "TP_BUZ_NM": "세부 업종명",
    "CSTMR_GUBUN": "고객 구분(내국인/외국인)",
    "CSTMR_MEGA_CTY_NO": "고객 거주 광역시도 코드",
    "CSTMR_MEGA_CTY_NM": "고객 거주 광역시도명",
    "CSTMR_CTY_RGN_NO": "고객 거주 시군구 코드",
    "CSTMR_CTY_RGN_NM": "고객 거주 시군구명",
    "SEX_CTGO_CD": "성별 코드(1=남, 2=여)",
    "AGE_VAL": "연령대",
    "FLC": "가족생애주기(Family Life Cycle) 코드",
    "AMT": "이용금액(원)",
    "CNT": "이용건수",
}


def describe_raw_bytes(path, encoding):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        raw = f.read()
    n_lf = raw.count(b"\n")
    n_cr = raw.count(b"\r")
    n_tab = raw.count(b"\t")
    header_text = raw[:300].decode(encoding, errors="replace")
    print(f"  - 파일 크기       : {size:,} bytes ({size/1024/1024:.1f} MB)")
    print(f"  - 인코딩(가정)     : {encoding}")
    print(f"  - LF(\\n) 개수     : {n_lf:,}")
    print(f"  - CR(\\r) 개수     : {n_cr:,}")
    print(f"  - TAB 개수        : {n_tab:,}")
    print(f"  - 줄바꿈 정상 여부 : {'정상' if n_lf > 1000 else '비정상 (줄바꿈 유실 의심)'}")
    print(f"  - 앞부분 미리보기  : {header_text[:200]!r}")


def main():
    print("=" * 80)
    print("[1] 파일별 원본 상태 점검 (bytes 단위)")
    print("=" * 80)
    for fname, enc in FILES.items():
        path = os.path.join(BASE_DIR, fname)
        print(f"\n### {fname}")
        describe_raw_bytes(path, enc)# 파일 설명해주는 코드

    print("\n" + "=" * 80)
    print("[2] 컬럼(스키마) 소개 - 23개 컬럼 공통")
    print("=" * 80)
    col_df = pd.DataFrame(
        {"컬럼명": list(COLUMN_DESC.keys()), "설명": list(COLUMN_DESC.values())}
    )
    print(col_df.to_string(index=False))

    print("\n" + "=" * 80)
    print("[3] 정상 파일(bc_card_out2020_03.txt) 샘플 확인 - pandas.read_csv")
    print("=" * 80)
    clean_path = os.path.join(BASE_DIR, "bc_card_out2020_03.txt")
    df_sample = pd.read_csv(clean_path, sep="\t", encoding="utf-8", nrows=5)
    print(df_sample)
    print("\n[dtypes]")
    print(df_sample.dtypes)

    print("\n" + "=" * 80)
    print("[4] 결론")
    print("=" * 80)
    print(
        "- bc_card_out2020_03.txt 는 정상적인 tab-separated 텍스트로 pandas.read_csv 로 바로 읽힘.\n"
        "- bc_card.txt 와 bc_card_output (1).txt 는 개행문자(\\n, \\r)가 전혀 없어 전체가 한 줄로\n"
        "  붙어있고, 레코드 사이 구분자도 없어(직전 레코드의 CNT 값과 다음 레코드의 REG_YYMM 값이\n"
        "  바로 이어붙음) read_csv 로 바로 읽을 수 없음 -> 02_preprocess.py 에서 정규식으로 복원 필요.\n"
        "- bc_card.txt(CP949) 와 bc_card_output (1).txt(UTF-8) 는 인코딩만 다를 뿐 완전히 동일한\n"
        "  2019년 6월 서울 데이터(레코드 수, 값 모두 동일)."
    )


if __name__ == "__main__":
    main()
