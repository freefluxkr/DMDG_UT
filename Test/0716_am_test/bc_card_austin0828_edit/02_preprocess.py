# -*- coding: utf-8 -*-
"""
02. 데이터 전처리
------------------
1) bc_card.txt(CP949, 개행 유실) 를 정규식으로 레코드 단위 복원 -> DataFrame
2) bc_card_output (1).txt(UTF-8, 개행 유실) 로 복원 결과를 교차 검증(동일 데이터인지 확인)
3) bc_card_out2020_03.txt(정상) 를 read_csv 로 로드
4) 두 시점(2019-06 / 2020-03) 을 동일 조건(서울특별시) 으로 맞추고 형 변환·정합성 점검
5) 전처리 완료 데이터를 data_processed/ 에 저장 (03_analysis.py 에서 재사용)
"""
import os
import re
import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUT_DIR = os.path.join(BASE_DIR, "data_processed")

NUMERIC_COLS = [
    "REG_YYMM", "MEGA_CTY_NO", "CTY_RGN_NO", "ADMI_CTY_NO",
    "MAIN_BUZ_CODE", "TP_GRP_NO", "TP_BUZ_NO",
    "CSTMR_MEGA_CTY_NO", "CSTMR_CTY_RGN_NO",
    "SEX_CTGO_CD", "FLC", "AMT", "CNT",
]

# 레코드 시작 앵커: REG_YYMM(6자리 숫자) + MEGA_CTY_NO(2자리 숫자) + MEGA_CTY_NM(한글) + 탭
RECORD_ANCHOR = re.compile(r"(\d{6})\t(\d{2})\t([가-힣]+)\t")


def reconstruct(path, encoding):
    """개행문자가 유실된 파일을 레코드 앵커 정규식으로 복원해 DataFrame으로 변환."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode(encoding)

    matches = list(RECORD_ANCHOR.finditer(text))
    starts = [m.start() for m in matches]
    header = text[: starts[0]].split("\t")

    records = []
    for i in range(len(starts)):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        records.append(text[starts[i]: end].split("\t"))

    n_cols = len(header)
    bad = [r for r in records if len(r) != n_cols]
    if bad:
        raise ValueError(f"컬럼 수가 맞지 않는 레코드 {len(bad)}건 발견 (복원 실패 의심)")

    df = pd.DataFrame(records, columns=header)
    return df


def cast_dtypes(df):
    df = df.copy()
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="raise")
    obj_cols = [c for c in df.columns if c not in NUMERIC_COLS]
    for col in obj_cols:
        df[col] = df[col].str.strip()
    return df


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("=" * 80)
    print("[1] bc_card.txt (CP949) 복원")
    print("=" * 80)
    df_2019_cp949 = reconstruct(os.path.join(BASE_DIR, "../data/bc_card.txt"), "cp949")
    print(f"  복원된 레코드 수: {len(df_2019_cp949):,}")
    print(df_2019_cp949.head(3))

    print("\n" + "=" * 80)
    print("[2] bc_card_output (1).txt (UTF-8) 복원 후 교차 검증")
    print("=" * 80)
    df_2019_utf8 = reconstruct(
        os.path.join(BASE_DIR, "bc_card_output (1).txt"), "utf-8"
    )
    print(f"  복원된 레코드 수: {len(df_2019_utf8):,}")
    is_identical = df_2019_cp949.reset_index(drop=True).equals(
        df_2019_utf8.reset_index(drop=True)
    )
    print(f"  bc_card.txt 와 값이 완전히 동일한가? -> {is_identical}")
    if not is_identical:
        raise ValueError("두 파일의 복원 결과가 다릅니다. 확인이 필요합니다.")

    print("\n" + "=" * 80)
    print("[3] 형 변환 및 정합성 점검 (2019-06)")
    print("=" * 80)
    df_2019 = cast_dtypes(df_2019_cp949)
    print(df_2019.dtypes)
    print(f"\n  결측치 총합: {df_2019.isna().sum().sum()}")
    print(f"  완전 중복행 수: {df_2019.duplicated().sum()}")
    print(f"  AMT<0 또는 CNT<0 인 행: {((df_2019['AMT'] < 0) | (df_2019['CNT'] < 0)).sum()}")
    print(f"  REG_YYMM 유일값: {sorted(df_2019['REG_YYMM'].unique())}")
    print(f"  MEGA_CTY_NM 유일값: {df_2019['MEGA_CTY_NM'].unique()}")

    print("\n" + "=" * 80)
    print("[4] bc_card_out2020_03.txt 로드 및 서울 필터링")
    print("=" * 80)
    df_2020_all = pd.read_csv(
        os.path.join(BASE_DIR, "../data/bc_card_out2020_03.txt"), sep="\t", encoding="utf-8"
    )
    print(f"  전국 전체 레코드 수: {len(df_2020_all):,}")
    print(f"  결측치 총합: {df_2020_all.isna().sum().sum()}")
    print(f"  완전 중복행 수: {df_2020_all.duplicated().sum()}")

    df_2020 = df_2020_all[df_2020_all["MEGA_CTY_NM"] == "서울특별시"].reset_index(drop=True)
    for col in df_2020.select_dtypes(include="object").columns:
        df_2020[col] = df_2020[col].str.strip()
    print(f"  서울특별시 필터링 후 레코드 수: {len(df_2020):,}")

    print("\n" + "=" * 80)
    print("[5] 두 시점 비교 가능성 점검 (스키마/카테고리 일치 여부)")
    print("=" * 80)
    print(f"  컬럼 일치 여부: {list(df_2019.columns) == list(df_2020.columns)}")
    common_buz = set(df_2019["TP_BUZ_NM"]) & set(df_2020["TP_BUZ_NM"])
    only_2019 = set(df_2019["TP_BUZ_NM"]) - set(df_2020["TP_BUZ_NM"])
    only_2020 = set(df_2020["TP_BUZ_NM"]) - set(df_2019["TP_BUZ_NM"])
    print(f"  세부업종(TP_BUZ_NM) 공통: {len(common_buz)}개, 2019만: {len(only_2019)}개, 2020만: {len(only_2020)}개")

    print("\n" + "=" * 80)
    print("[6] 전처리 결과 저장")
    print("=" * 80)
    df_2019.to_pickle(os.path.join(OUT_DIR, "2019_06_seoul.pkl"))
    df_2020.to_pickle(os.path.join(OUT_DIR, "2020_03_seoul.pkl"))
    df_2019.head(200).to_csv(
        os.path.join(OUT_DIR, "2019_06_seoul_sample.csv"), index=False, encoding="utf-8-sig"
    )
    df_2020.head(200).to_csv(
        os.path.join(OUT_DIR, "2020_03_seoul_sample.csv"), index=False, encoding="utf-8-sig"
    )
    print(f"  저장 완료: {OUT_DIR}")
    print(f"    - 2019_06_seoul.pkl  ({len(df_2019):,} rows)")
    print(f"    - 2020_03_seoul.pkl  ({len(df_2020):,} rows)")


if __name__ == "__main__":
    main()
