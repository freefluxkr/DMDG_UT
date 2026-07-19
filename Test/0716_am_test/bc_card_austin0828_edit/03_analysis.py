# -*- coding: utf-8 -*-
"""
03. 데이터 분석 (시각화 없는 버전)
----------------------------------
전처리 완료된 서울 지역 카드소비 데이터(2019-06, 2020-03 각각)를 대상으로 아래 항목을 구한다.
차트(matplotlib) 없이 pandas 연산과 표 출력만 수행한다.

[대분류 1] 서울시 거주/비거주 고객의 소비 분석
  1. 서울시 거주/비거주 고객 수 구하기
  2. 총 소비액 구하기
  3. 성별 소비액 구하기

[대분류 2] 편의점 소비 정보 분석
  1. 편의점 소비액 구하기
  2. 강남구 편의점 소비액 분석하기
  3. 서울시 거주/비거주 고객의 소비액 구하기 (편의점 기준)
  4. 거주지 소재 편의점 소비액 구하기

* 이 데이터는 고객 개인 식별자(ID)가 없고, (행정동 x 업종 x 고객거주지 x 성별 x 연령대)
  조합별 월간 합계로 이미 집계되어 있다. 따라서 "고객 수"는 개인 수가 아니라
  총 이용건수(CNT) 합계로 근사한다.
* 2019-06(서울)과 2020-03(서울)은 표본 규모가 크게 달라(행 수 기준 약 15.9배) 두 시점을
  합쳐서 보면 왜곡되므로, 두 시점을 각각 따로 계산해 나란히 보여준다.
"""
import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data") #현재 디렉토리 위치
DATA_DIR = os.path.join(BASE_DIR, "data_processed") #전처리된 파일들 있는 디렉토리 위치

CONVENIENCE_STORE = "편 의 점"  # TP_BUZ_NM 원본 표기(내부 공백 포함) 그대로 사용해야 매칭됨
PERIODS = {"2019-06": "2019_06_seoul.pkl", "2020-03": "2020_03_seoul.pkl"}


def add_resident_flag(df):
    df = df.copy()
    df["거주구분"] = np.where(
        df["CSTMR_MEGA_CTY_NM"] == "서울특별시", "거주(서울)", "비거주(타지역)"
    )
    return df


def analyze_resident(df, period, results):# period는 기간
    print("\n" + "-" * 80)
    print(f"[대분류1] 서울시 거주/비거주 고객의 소비 분석 - {period}")
    print("-" * 80)
    df = add_resident_flag(df)#

    print("\n1. 서울시 거주/비거주 고객 수 구하기 (개인 ID가 없어 총 이용건수 CNT 합계로 근사)")
    cnt_by_res = df.groupby("거주구분")["CNT"].sum().rename("이용건수(CNT)")
    print(cnt_by_res.to_string())
    results[("resident_cnt", period)] = cnt_by_res

    print("\n2. 총 소비액 구하기")
    amt_by_res = df.groupby("거주구분")["AMT"].sum().rename("총소비액(AMT)")
    print(amt_by_res.to_string())
    results[("resident_amt", period)] = amt_by_res

    print("\n3. 성별 소비액 구하기 (거주구분 x 성별, 1=남성 2=여성 추정)")
    amt_by_res_sex = df.groupby(["거주구분", "SEX_CTGO_CD"])["AMT"].sum().unstack("SEX_CTGO_CD")
    print(amt_by_res_sex.to_string())
    results[("resident_sex_amt", period)] = amt_by_res_sex


def analyze_convenience(df, period, results):
    print("\n" + "-" * 80)
    print(f"[대분류2] 편의점 소비 정보 분석 - {period}")
    print("-" * 80)
    df = add_resident_flag(df)
    conv = df[df["TP_BUZ_NM"] == CONVENIENCE_STORE]

    print("\n1. 편의점 소비액 구하기")
    total_amt, total_cnt = conv["AMT"].sum(), conv["CNT"].sum()
    print(f"  총 소비액(AMT): {total_amt:,}원 / 총 이용건수(CNT): {total_cnt:,}건")
    results[("conv_total", period)] = pd.Series({"AMT": total_amt, "CNT": total_cnt})

    print("\n2. 강남구 편의점 소비액 분석하기")
    gn = conv[conv["CTY_RGN_NM"] == "강남구"]
    gn_amt, gn_cnt = gn["AMT"].sum(), gn["CNT"].sum()
    share = gn_amt / total_amt * 100 if total_amt else float("nan")
    print(f"  강남구 편의점 소비액: {gn_amt:,}원 / 이용건수: {gn_cnt:,}건")
    print(f"  전체 편의점 소비액 대비 강남구 비중: {share:.2f}%")
    top_res = (
        gn.groupby("CSTMR_CTY_RGN_NM")["AMT"].sum().sort_values(ascending=False).head(5)
    )
    print("  강남구 편의점 이용 고객의 거주지 TOP5:")
    print(top_res.to_string())
    results[("conv_gangnam", period)] = pd.Series(
        {"AMT": gn_amt, "CNT": gn_cnt, "전체대비비중(%)": share}
    )
    results[("conv_gangnam_customer_origin_top5", period)] = top_res

    print("\n3. 서울시 거주/비거주 고객의 소비액 구하기 (편의점 기준)")
    conv_res_amt = conv.groupby("거주구분")["AMT"].sum().rename("편의점 소비액(AMT)")
    print(conv_res_amt.to_string())
    results[("conv_resident_amt", period)] = conv_res_amt

    print("\n4. 거주지 소재 편의점 소비액 구하기 (고객 거주 구 == 편의점 소재 구)")
    local = conv[conv["CSTMR_CTY_RGN_NM"] == conv["CTY_RGN_NM"]]
    other = conv[conv["CSTMR_CTY_RGN_NM"] != conv["CTY_RGN_NM"]]
    local_amt, other_amt = local["AMT"].sum(), other["AMT"].sum()
    local_share = local_amt / total_amt * 100 if total_amt else float("nan")
    print(f"  거주지 소재 편의점 소비액: {local_amt:,}원 ({local_share:.2f}%)")
    print(f"  타지역 편의점 소비액: {other_amt:,}원 ({100 - local_share:.2f}%)")
    results[("conv_local_vs_other", period)] = pd.Series(
        {"거주지소재": local_amt, "타지역": other_amt}
    )


def main():
    dfs = {p: pd.read_pickle(os.path.join(DATA_DIR, f)) for p, f in PERIODS.items()} # PERIODS.items()->연도:파일 형식의 딕셔너리 dfs -> 연도:
    results = {}

    for period, df in dfs.items(): #연도별 분석
        analyze_resident(df, period, results)
        analyze_convenience(df, period, results)

    # ---- 결과 저장(CSV) ----
    for (name, period), obj in results.items():
        fname = f"result_{name}_{period.replace('-', '')}.csv"
        obj.to_csv(os.path.join(DATA_DIR, fname), encoding="utf-8-sig")

    print("\n모든 결과(CSV) 저장 완료:", DATA_DIR)


if __name__ == "__main__":
    main()
