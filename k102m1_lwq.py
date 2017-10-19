# ----------code
import numpy as np
import pandas as pd

import zwSys as zw
import zwTools as zwt


def zw_anz_m1sub(stkCode, path, month):
    """
    :param stkCode: 股票代号
    :param path: 数据文件存放的目录 'zwDat/cn/xday/'
    :param month: 指定月份 ‘01’～'12'
    :return: numSum, numInc, numDec  所有月份累计，上涨月份累计，下跌月份累计
    """
    filename = path + stkCode + ".csv"  # 'zwDat/cn/xday/000001.csv'

    numSum, numInc, numDec = 0, 0, 0  # 输入的月份数，其中上升的月份，其中下跌的月份

    # print(filename)
    try:
        df = pd.read_csv(filename, index_col=0, parse_dates=[0], encoding='utf-8')
        # 读取数据文件，第一列指定为索引列，并解析为日期类型
        df = df.rename(columns={'Close': 'close'})  # 如果列名是Close，则改名，收盘价
        df = df.sort_index()  # 按日期排序

        startTime = df.index[0]  # 取得时间列的第一行
        startYear = startTime.year  # 截取第一行的年份
        endTime = df.index[-1]  # 取得时间列的最后一行
        endYear = endTime.year  # 最后一年

        for year in range(startYear, endYear+1):  # 遍历所有年份
            year = str(year)  # 年份
            last_day = zwt.lastDay(year, int(month))  # 年份，每月的最后一天的日期
            day = '%02d' % last_day
            firstDate = ''.join([year, '-', month, '-01'])  # 当前月的第一天
            lastDate = ''.join([year, '-', month, '-', day])  # 当前月的最后一天
            df_oneMonth = df[(df.index >= firstDate) & (df.index <= lastDate)]
            # 提取月初到月底之间的数据
            """
            if len(df_oneMonth) > 0:  # 若存在交易日（处理月份用）
                _kmon5 = '%02d' % df_oneMonth.index[0].month  # 选取交易日期中的月份，并转为string
                if _kmon5 == month:  # 若上述月份为函数输入的变量
                    firstRecoder = df_oneMonth.iloc[0]  # 月初首条记录
                    lastRecoder = df_oneMonth.iloc[-1]  # 月末最后一条记录
                    numSum += 1  # 所有月份累计
                    firstClose = firstRecoder['close']  # 月初的收盘价
                    lastClose = lastRecoder['close']  # 月末的收盘价
                    if lastClose > firstClose:
                        numInc += 1  # 比较收盘价位，判定升跌
                    else:
                        numDec += 1
            """
            firstRecoder = df_oneMonth.iloc[0]  # 月初首条记录
            lastRecoder = df_oneMonth.iloc[-1]  # 月末最后一条记录
            numSum += 1  # 所有月份累计
            firstClose = firstRecoder['close']  # 月初的收盘价
            lastClose = lastRecoder['close']  # 月末的收盘价
            if lastClose > firstClose:
                numInc += 1  # 比较收盘价位，判定升跌
            else:
                numDec += 1
    except IOError:
        print('CSV文件不存在，跳过')
        pass  # 跳过，不处理

    # print('numSum,numInc,numDec = ', numSum, numInc, numDec)
    return numSum, numInc, numDec  # 返回值为所有月份累计，上升月份，下跌月份统计


def zw_stk_anz_m01(qx, inxFile, path, month):
    """
    对每个股票运算一次上一个函数
    :param qx: 环境变量，zwDat目录位置
    :param inxFile: 从股票种类列表中提取的股票名称，用于文件读取
    :param path: 数据文件存放的目录 'zwDat/cn/xday/'
    :param month: 指定月份
    :return: monTotal 包含指定月份的统计数据的字典
    """
    filename = qx.rdatInx + inxFile + ".csv"  # filename = zwDat/inx/inx_code.csv

    codeType = 'gbk'
    if path.find('us') > 0:
        codeType = 'utf-8'
    # print('文件路径及文件编码： ', filename, codeType)

    df = pd.read_csv(filename, encoding=codeType)  # 读取csv文件

    print(df.head())
    print('文件路径： ',filename)

    monTotal = dict()
    monTotal['inxFile'] = inxFile  # 股票种类 in_code
    monTotal['month'] = month  # 月份 01~12
    monTotal['numSum'] = 0  # 总数合计
    monTotal['numInc'] = 0  # 上涨数合计
    monTotal['numDec'] = 0  # 下跌数合计

    numLine = len(df['code'])
    monTotal['numStk'] = numLine  # 股票总行数

    for i, stkCode in enumerate(df['code']):  # 遍历当前类别的股票代码
        if not isinstance(stkCode, str):  # 非正常股票代码处理
            stkCode = "%06d" % stkCode

        # print(stkCode, path, month)
        dSum, dAdd, dDec = zw_anz_m1sub(stkCode, path, month)

        monTotal['numSum'] = monTotal['numSum'] + dSum
        monTotal['numInc'] = monTotal['numInc'] + dAdd
        monTotal['numDec'] = monTotal['numDec'] + dDec
        # print(i, '/', xn9, stkCode, monTotal)

    monTotal['preInc'] = np.round(monTotal['numInc'] * 100 / monTotal['numSum'])  # 上涨百分比
    monTotal['preDec'] = np.round(monTotal['numDec'] * 100 / monTotal['numSum'])  # 下跌百分比

    # print(monTotal)
    return monTotal


def zw_stk_anz_mx(qx, inxFile, path):
    """
    将一个类别的股票，生成一个csv文件
    :param qx: 环境变量，zwDat目录位置
    :param inxFile: 从股票种类列表中提取的股票名称，用于输出CSV文件名
    :param path: 数据文件存放的目录 'zwDat/cn/xday/'
    :return: 空
    """
    fields = [  # 构造csv文件的字段名
        'inxFile'  # 股票类别名称
        , 'month'  # 当前月份
        , 'numStk'  # 当前类别种股票支数
        , 'numSum'  # 所有月份累计
        , 'numInc'  # 上涨月份累计
        , 'numDec'  # 下跌月份累计
        , 'preInc'  # 上涨百分比
        , 'preDec'  # 下跌百分比
    ]

    df = pd.DataFrame(columns=fields)  # 定义dataframe
    filename = "temp/monTotal_" + inxFile + ".csv"  # 将要保存csv文件的路径
    print('csv文件的路径: ' + filename)

    for i in range(12):
        month = "%02d" % (i + 1)  # 两位表示的月份

        monTotal = zw_stk_anz_m01(qx, inxFile, path, month)  # 当前股票类别当前月的涨跌统计 字典

        ds = pd.Series(monTotal, index=fields)  # 将字典内容转成一列数据
        ds = ds.T  # 将列数据转成行数据
        df = df.append(ds, ignore_index=True)  # 将行数据添加到dataframe中
        # break
    # print(df.head())
    df.to_csv(filename, index=False, encoding='utf-8')  # 将dataframe数据存盘csv


def zw_stk_anz_mx_all(qx, xlist):
    """
    遍历股票类别list中的股票，提取列表项逐个调用函数处理
    :param qx: 环境变量，zwDat目录位置
    :param xlist: 股票类别列表
    :return: 空
    """
    for inxFile in xlist:
        if inxFile.find('Yah') > 0:
            path = qx.rdat + 'us/day/'  # path = zwDat/us/xday/
        else:
            if inxFile == 'inx_code':
                path = qx.rdat + 'cn/xday/'  # path = zwDat/cn/xday/ 指数数据
            else:
                path = qx.rdat + 'cn/Day/'  # path = zwDat/cn/day/ 个股数据

        print('参数 qx.rdat inxFile path = ', qx.rdat, inxFile, path)
        zw_stk_anz_mx(qx, inxFile, path)  # 生成csv文件


def main():
    qx = zw.zwDatX(zw._rdat0)  # 初始化环境变量

    # uslist = [
    #     'inxYahoo30sp'  # 道琼斯30指数美股代码
    #     , 'inxYahoo100ns'  # 纳斯达克100指数美股代码
    #     , 'inxYahoo100sp'  # 道琼斯100工业指数美股代码
    #     , 'inxYahoo600'  # 量化常用美股600股票代码
    #     , 'inxYahoo500sp'  # 道琼斯500指数美股代码
    #     , 'inxYahoo'  # 全部6688美股代码
    # ]
    # zw_stk_anz_mx_all(qx, uslist)

    cnlist = [
        'inx_code'  # 中国A股大盘及各种指数代码
        , 'stk_sz50'  # 中国上证50指数股票代码
        , 'stk_hs300'  # 中国沪深300指数股票代码
        , 'stk_zz500'  # 中国中证500指数股票代码
        , 'stk_code'  # 中国A股2810只股票代码
    ]
    zw_stk_anz_mx_all(qx, cnlist)

    print('全部处理完成')


if __name__ == '__main__':
    main()

