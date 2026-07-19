import pandas as pd
import numpy as np

def func1():

    df = pd.DataFrame()

    with open("../data/bc_card_output.txt", 'r', encoding='utf-8') as f:
        tokens = f.read().split("\t")

        row_len = len(tokens)/23
        row_len -= 1
        head = tokens[0:23]
        head[-1] = head[-1].split('\n')[0].split('\r')[0]
        datas = []
        tt = head[-1]
        head[-1] = tt[:-6]
        datas.append(tt[-6:])

        total = 1
        for r in range(23, len(tokens)):
            if total %23 ==0 and total!=0:
                temp = datas[-1]
                datas[-1] = temp[:-6]
                datas.append(temp[-6:])
                total+=1
            datas.append(tokens[r])
            total += 1

        arr = np.array(datas)
        aa = arr.reshape(-1, 23)

        df = pd.DataFrame(aa, columns=head)


    # for col in df.columns:
    #     print(col)
    print(df.info())
    # print('#'*30)
    # print(df.isna().sum())
    #결측치 없음을 확인
    #print(df.head())

    print(df.head(2))

    #print(df.groupby('MEGA_CTY_NM').count())

    def is_seoul(str):
        if str == '서울특별시':
            return 1
        return 0

    #df['is_seoul'] = df['CSTMR_MEGA_CTY_MM'].apply(is_seoul)
    seoul = df[df['MEGA_CTY_NM'] == '서울특별시']

    print(f"서울:{seoul.size}, 비서울: {df.size- seoul.size}")

    def convert_string_to_int(str):
        return int(str)

    df['AMT'] = df['AMT'].apply(convert_string_to_int)
    total_consume = df['AMT'].sum()
    print(f"소비 합: {total_consume}")

    sex_consume = df.groupby('SEX_CTGO_CD')['AMT'].sum()
    print(f"성별 소비:\n {sex_consume}")



def func2():
    df = pd.read_csv("../data/bc_card_out2020_03.txt", sep='\t')

    # 편의점이 어느 업종 컬럼(대/중/소분류)에 들어있는지 자동 탐색
    
    print(df.columns)
    print(df.head())
    conv = df[df['TP_BUZ_NM'] == '편 의 점']
    
    #  편의점 소비액
    print("편의점 소비: ", conv['AMT'].sum())
    
    #  강남구(가맹점 소재) 편의점 소비액
    print("강남 편점 소비: ", conv[conv['CTY_RGN_NM'] == '강남구']['AMT'].sum())
    
    #  서울시 거주/비거주 고객 소비액
    res = conv['CSTMR_MEGA_CTY_NM'] == '서울특별시'
    
    print(conv.groupby(res.map({True:'거주', False:'비거주'}))['AMT'].sum())
    
    # ④ 거주지 소재 편의점 소비액 (가맹점 시군구 == 고객 거주 시군구, 코드로 매칭)
    same = conv['CTY_RGN_NO'] == conv['CSTMR_CTY_RGN_NO']
    print("거주지 소재 편점 소비", conv.loc[same, 'AMT'].sum())

if __name__ == '__main__':
    func1()
    func2()