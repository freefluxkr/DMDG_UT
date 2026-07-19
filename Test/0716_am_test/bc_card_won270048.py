"""
카드 소비 데이터 분석 (판다스만 사용)
- bc_card.txt / bc_card_output.txt : 2019-06 데이터 (개행 유실 -> 복구 필요, 서로 동일한 데이터)
- bc_card_out2020_03.txt          : 2020-03 데이터 (정상 포맷)
"""
import pandas as pd

COLS = ["REG_YYMM", "MEGA_CTY_NO", "MEGA_CTY_NM", "CTY_RGN_NO", "CTY_RGN_NM", "ADMI_CTY_NO", "ADMI_CTY_NM",
        "MAIN_BUZ_CODE", "MAIN_BUZ_DESC", "TP_GRP_NO", "TP_GRP_NM", "TP_BUZ_NO", "TP_BUZ_NM", "CSTMR_GUBUN",
        "CSTMR_MEGA_CTY_NO", "CSTMR_MEGA_CTY_NM", "CSTMR_CTY_RGN_NO", "CSTMR_CTY_RGN_NM", "SEX_CTGO_CD",
        "AGE_VAL", "FLC", "AMT", "CNT"] # -> 총 23개!!!
HEADER_STR = "\t".join(COLS)

print(HEADER_STR)
print(type(HEADER_STR))

def reconstruct_broken_file(path, encoding, n_records, reg_yymm="201906"):
    """bc_card.txt/bc_card_output.txt에서 유실된 개행문자를 복구하여 DataFrame으로 반환."""
    with open(path, encoding=encoding) as f:
        data = f.read()
    assert data.startswith(HEADER_STR)
    parts = data[len(HEADER_STR):].split("\t")

    pointer, carry, records = 0, None, []
    for i in range(n_records):
        row = []
        if carry is not None:
            row.append(carry);
            carry = None
        else:
            row.append(parts[pointer]);
            pointer += 1
        for _ in range(21):
            row.append(parts[pointer]);
            pointer += 1
        last_field = parts[pointer];
        pointer += 1
        if i < n_records - 1:
            idx = last_field.rfind(reg_yymm)
            row.append(last_field[:idx])
            carry = last_field[idx:]
        else:
            row.append(last_field)
        records.append(row)
    assert pointer == len(parts)
    df = pd.DataFrame(records, columns=COLS)
    df["AMT"] = df["AMT"].astype("int64")
    df["CNT"] = df["CNT"].astype("int64")
    return df


def load_clean_file(path):
    dtype_map = {c: "category" for c in COLS if c not in ("AMT", "CNT")}
    dtype_map.update({"AMT": "int64", "CNT": "int64"})
    df = pd.read_csv(path, sep="\t", dtype=dtype_map, encoding="utf-8")
    for c in df.columns:
        if df[c].dtype.name == "category":
            df[c] = df[c].astype(str)
    return df


if __name__ == "__main__":
    # 1) 손상 파일 복구 (100,001건, 2019-06) - 두 파일은 동일 데이터이므로 하나만 사용
    df_2019_06 = reconstruct_broken_file(
        r"C:\Users\enjoy\PycharmProjects\PythonProject\0714\bc_card_output.txt", encoding="utf-8", n_records=100001
    )

    # 2) 정상 파일 로드 (1,589,494건, 2020-03)
    df_2020_03 = load_clean_file(r"C:\Users\enjoy\PycharmProjects\PythonProject\0714\bc_card_out2020_03.txt")

    # 3) 데이터 결합
    df = pd.concat([df_2019_06, df_2020_03], ignore_index=True)

    # 4) 파생 변수
    df["거주구분"] = df["CSTMR_MEGA_CTY_NM"].apply(
        lambda x: "서울시 거주" if x == "서울특별시" else "서울시 비거주"
    )
    df["성별"] = df["SEX_CTGO_CD"].map({"1": "남성", "2": "여성"})

    # ── 3-1. 서울시 거주/비거주 고객의 소비 분석 ─────────────────────
    print("① 거주/비거주 이용건수(CNT) 합계")
    print(df.groupby("거주구분")["CNT"].sum(), "\n")

    print("② 거주/비거주 총 소비액(AMT)")
    print(df.groupby("거주구분")["AMT"].sum(), "\n")

    print("③ 성별 소비액")
    print(df.groupby("성별")["AMT"].sum(), "\n")
    print(df.groupby(["거주구분", "성별"])["AMT"].sum(), "\n")

    # ── 3-2. 편의점 소비 정보 분석 ─────────────────────────────────
    cvs = df[df["TP_BUZ_NM"] == "편 의 점"].copy()

    print("① 편의점 소비액")
    print(cvs.groupby("REG_YYMM")[["AMT", "CNT"]].sum(), "\n")
    print("전체 편의점 소비액:", cvs["AMT"].sum(), "\n")

    print("② 강남구 편의점 소비액 분석")
    gn = cvs[cvs["CTY_RGN_NM"] == "강남구"]
    print("강남구 편의점 소비액:", gn["AMT"].sum())
    print(cvs.groupby("CTY_RGN_NM")["AMT"].sum().sort_values(ascending=False).head(), "\n")

    print("③ 거주/비거주 고객의 편의점 소비액")
    print(cvs.groupby("거주구분")[["AMT", "CNT"]].sum(), "\n")

    print("④ 거주지 소재 편의점 소비액")
    same_gu = cvs[
        (cvs["CSTMR_MEGA_CTY_NM"] == "서울특별시")
        & (cvs["CTY_RGN_NM"] == cvs["CSTMR_CTY_RGN_NM"])
        ]
    print("거주지 소재 편의점 소비액:", same_gu["AMT"].sum())