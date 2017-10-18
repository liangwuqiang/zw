# ----------code
import numpy as np
import pandas as pd

import zwSys as zw
import zwTools as zwt


def zw_anz_m1sub(xcod, rss, monStr):
    """
    :param xcod: 股票代号
    :param rss: 存放目录 'zwDat/cn/xday/'
    :param monStr: 当前月份 ‘01’
    :return:
    """
    fss = rss + xcod + ".csv"  # 'zwDat/cn/xday/000001.csv'
    print(fss)  # 文件名

    nSum, nAdd, nDec = 0, 0, 0  # 输入的月份数，其中上升的月份，其中下跌的月份
    kmon = int(monStr)  # 当前月份

    try:
        df = pd.read_csv(fss, index_col=0, parse_dates=[0], encoding='utf-8')
        # 读取数据文件，第一列指定为索引列，并解析为日期类型
        df = df.rename(columns={'Close': 'close'})  # 如果列名是Close，则改名，收盘价
        df = df.sort_index()  # 按日期排序

        _tim0 = df.index[0]  # 取得时间列的第一行
        _ynum0 = _tim0.year  # 截取第一行的年份
        _tim9 = df.index[-1]  # 取得时间列的最后一行
        _ynum9 = _tim9.year + 1  # 最后一年+1

        for ynum in range(_ynum0, _ynum9):  # 遍历所有年份
            ystr = str(ynum)  # 年份
            print(ystr)
            last_day = zwt.lastDay(ynum, kmon)  # 年份，每月的最后一天的日期
            print(last_day)
            dayStr = '%02d' % last_day
            monStr1 = ''.join([ystr, '-', monStr, '-01'])  # 当前月的第一天
            monStr9 = ''.join([ystr, '-', monStr, '-', dayStr])  # 当前月的最后一天
            df2 = df[(df.index >= monStr1) & (df.index <= monStr9)]
            # 月初到月底之间的数据

            if len(df2) > 0:  # 若存在交易日（处理月份用）
                _kmon5 = '%02d' % df2.index[0].month  # 选取交易日期中的月份，并转为string
                if _kmon5 == monStr:  # 若上述月份为函数输入的变量
                    xd1a = df2.ix[0]
                    xd1z = df2.ix[-1]
                    nSum += 1  # 交易月份+1
                    vd1a = xd1a['close']
                    vd1z = xd1z['close']  # 选取收盘价位
                    if vd1z > vd1a:
                        nAdd += 1  # 比较收盘价位，判定升跌
                    else:
                        nDec += 1

    except IOError:
        pass  # skip,error

    print('nSum,nAdd,nDec,', nSum, nAdd, nDec)
    return nSum, nAdd, nDec  # 返回值为交易月份数量，上升，下跌


def zw_stk_anz_m01(qx, finx0, rss, ksgn):  # 对每个股票运算一次上一个函数
    fss = qx.rdatInx + finx0 + ".csv"  # stk_code.csv,inxYahoo.csv

    codTyp = 'gbk'
    if rss.find('us') > 0:
        codTyp = 'utf-8'
    # print('f', fss, codTyp)

    dinx = pd.read_csv(fss, encoding=codTyp)  # 读取csv文件

    # print(dinx.head())
    # print('f2',fss)

    mx1 = dict()
    mx1['finx'] = finx0
    mx1['ksgn'] = ksgn
    mx1['nSum'] = 0
    mx1['nAdd'] = 0
    mx1['nDec'] = 0  # 字典，赋值

    xn9 = len(dinx['code'])
    mx1['nstk'] = xn9  # 所读取的csv的行数（code列的长度）

    # 遍历csv中的code名,i 是计数器变量
    for i, xcod in enumerate(dinx['code']):
        if not isinstance(xcod, str):
            xcod = "%06d" % xcod

        dSum, dAdd, dDec = zw_anz_m1sub(xcod, rss, ksgn)

        mx1['nSum'] = mx1['nSum'] + dSum
        mx1['nAdd'] = mx1['nAdd'] + dAdd
        mx1['nDec'] = mx1['nDec'] + dDec
        # print(i, '/', xn9, xcod, mx1)
    #
    # print('xn9', xn9)  # print(len(mx1['nAdd']))
    print('------')
    # mx1['kAdd'] = np.round(mx1['nAdd'] * 100 / mx1['nSum'])  # 指数上升频率（估计概率）
    # mx1['kDec'] = np.round(mx1['nDec'] * 100 / mx1['nSum'])  # 指数下降频率（估计概率）

    return mx1


def zw_stk_anz_mx(qx, finx0, rss):  # 生成一个csv文件
    c10 = [  # csv的第一列
        'finx'
        , 'ksgn'
        , 'nstk'
        , 'nSum'
        , 'nAdd'
        , 'nDec'
        , 'kAdd'
        , 'kDec'
    ]

    df = pd.DataFrame(columns=c10)  # 定义dataframe
    ftg = "tmp/mx_" + finx0 + ".csv"
    # print(ftg)  # 打印csv文件名

    # for i in range(12):
    for i in range(1):
        ksgn = "%02d" % (i + 1)

        mx1 = zw_stk_anz_m01(qx, finx0, rss, ksgn)  # 利用上一个函数生成一个dataframe,

        # ds1 = pd.Series(mx1, index=c10)  # 生成一个pandas中的series
        # ds2 = ds1.T  # .T = 转置（矩阵转置）
        # df = df.append(ds2, ignore_index=True)  # 在df中加上ds2
        # df.to_csv(ftg, index=False, encoding='utf8')  # 保存为csv，utf8编码


def zw_stk_anz_mx_all(qx, xlst):  # 遍历指定list中的股票
    for fx in xlst:
        if fx.find('Yah') > 0:
            # rss=qx.rZWusDay
            rss = qx.rdat + 'us/day/'
        else:
            if fx == 'inx_code':
                rss = qx.rdat + 'cn/xday/'  # rss=qx.rZWcnXDay
            else:
                rss = qx.rdat + 'cn/day/'  # rss=qx.rZWcnDay

        finx0 = fx  # 生成文件名
        zw_stk_anz_mx(qx, finx0, rss)  # 用上一个函数生成csv文件
        # print(qx.rdat, finx0, rss)


def main():
    qx = zw.zwDatX(zw._rdat0)  # 初始化变量

    # uslst = [
    #     'inxYahoo30sp'  # 道琼斯30指数美股代码
    #     , 'inxYahoo100ns'  # 纳斯达克100指数美股代码
    #     , 'inxYahoo100sp'  # 道琼斯100工业指数美股代码
    #     , 'inxYahoo600'  # 量化常用美股600股票代码
    #     , 'inxYahoo500sp'  # 道琼斯500指数美股代码
    #     , 'inxYahoo'  # 全部6688美股代码
    # ]
    # zw_stk_anz_mx_all(qx, uslst)

    cnlst = [
        'inx_code'  # 中国A股大盘及各种指数代码
        # , 'stk_sz50'  # 中国上证50指数股票代码
        # , 'stk_hs300'  # 中国沪深300指数股票代码
        # , 'stk_zz500'  # 中国中证500指数股票代码
        # , 'stk_code'  # 中国A股2810只股票代码
        # , 'stk_code'  #
    ]
    zw_stk_anz_mx_all(qx, cnlst)


if __name__ == '__main__':
    main()

