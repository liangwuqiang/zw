import pandas as pd


def zw_anz_m1sub(stkCode, path, month):
    filename = path + stkCode + ".csv"
    print(filename)
    nSum, nAdd,nDec = 0, 0, 0
    intMonth = int(month)
    knum2 = intMonth + 1  #//////////////////////
    
    df = pd.read_csv(filename,index_col=0,parse_dates=[0],encoding='utf-8')
    df = df.rename(columns={'Close':'close'})
    df = df.sort_index()

    startTime = df.index[0]
    startYear = startTime.year
    endTime = df.index[-1]
    endYear = endTime.year

    for ynum in range(startYear, endYear + 1):
        ystr = str(ynum)  # 2015
        # _tim1x = '-1'
        ystr2 = ystr + "-" + month  # 2015-01
        # print(ystr2, len(df), intMonth)
        if intMonth == 12:
            ystr3 = ystr + "-" + month + '-31'  # 2015-12-31
            # print(ystr3)
            df2 = df[(df.index >= ystr2)&(df.index <= ystr3)]
            # print(df2)
        else:
            kstr2 = str(knum2)
            print(knum2, kstr2)
            if knum2 < 10:
                kstr2 = '0' + kstr2
            ystr3 = ystr + "-" + kstr2 + '-01'  # 2015-02-01
            print(ystr3)
            df2 = df[(df.index >= ystr2)&(df.index < ystr3)]
        # print(ystr2,ystr3,len(df2))
        # if len(df2)>0:
        #     _tim1x = str(df2.index[0].month)
        #     if len(_tim1x)<2:
        #         _tim1x = '0' + _tim1x
        # if _tim1x == month:
        #     df1 = df2[ystr2]
        #     if len(df1)>0:
        #         xd1a = df1.ix[0]
        #         xd1z = df1.ix[-1]
        #         nSum  += 1
        #         vd1a = xd1a['close']
        #         vd1z = xd1z['close']
        #         if vd1z>vd1a:
        #             nAdd  += 1
        #         else:
        #             nDec  += 1
                   
    return nSum,nAdd,nDec    
   
def main():
    
    # root  =  './zwDat/'
    # myZwDatX  =  zw.zwDatX(root)  # 用数据文件根目录实例化zwDatX类
    
    stkCode = "002739" #万达院线
    path = './zwDat/cn/' + 'Day/'
    month = "01"  # 月份
    nSum,nAdd,nDec = zw_anz_m1sub(stkCode, path, month)
    # print('nSum,nAdd,nDec',nSum,nAdd,nDec)

if __name__ == '__main__':
    main()