
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('seaborn-whitegrid')

def mx_sum_main(inxList):

    # df = pd.DataFrame(index=months, columns=inxList)
    df = pd.DataFrame(columns=inxList)

    for item in inxList:
        filename = './temp/monTotal_' + item + '.csv'
        # print(filename)
        df_csv = pd.read_csv(filename, encoding='utf-8')
        df[item] = df_csv['preInc']

    df.index = [i + 1 for i in range(12)]

    print(df)

    return df


def main():
    cnList = [  # 中国股市
        'inx_code'  # 中国A股大盘及各种指数代码
        , 'stk_sz50'  # 中国上证50指数股票代码
        , 'stk_hs300'  # 中国沪深300指数股票代码
        , 'stk_zz500'  # 中国中证500指数股票代码
        , 'stk_code'  # 中国A股2810只股票代码
    ]
    df = mx_sum_main(cnList)

    df.plot(kind='line', colormap='hot', rot=0, figsize=(20, 5))
    plt.legend(ncol=3,loc=2)
    plt.tight_layout()
    plt.show()
    
    # 美国股市
    # usList=['xYah30sp','xYah100ns','xYah100sp','xYah600','xYah500sp','xYah']
    # df = mx_sum_main(usList)
    # df.plot(kind='bar',colormap='hot',rot=0,figsize=(20,5))
    # plt.legend(ncol=3,loc=2)
    # plt.tight_layout()

if __name__ == '__main__':
    main()