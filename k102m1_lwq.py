
import os
import numpy as np
import pandas as pd

import zwSys as zw
import zwTools as zwt  # 用于获取每月最后一天


def zw_anz_m1sub(stkCode, path, month):
    """
    单只股票的当前月份统计
    :param stkCode: 股票代号
    :param path: 数据文件存放的目录 './zwDat/cn/xday/'
    :param month: 指定当前月份 ‘01’～'12'
    :return: numSum, numInc, numDec  当前月份合计，上涨月份合计，下跌月份合计
    """
    filename = path + stkCode + ".csv"  # './zwDat/cn/xday/000001.csv'
    # print(filename)

    numSum, numInc, numDec = 0, 0, 0  # 变量初始化

    try:
        df = pd.read_csv(filename, index_col=0, parse_dates=[0], encoding='utf-8')
        # 读取数据文件，第一列指定为索引列，并解析为日期类型
        df = df.rename(columns={'Close': 'close'})  # 针对美国股市
        df = df.sort_index()  # 按日期排序

        startTime = df.index[0]  # 取得时间列的第一行
        startYear = startTime.year  # 截取第一行的年份
        endTime = df.index[-1]  # 取得时间列的最后一行
        endYear = endTime.year  # 最后一年

        for year in range(startYear, endYear+1):  # 遍历所有年份

            last_day = zwt.lastDay(year, int(month))  # 获取每月的最后一天的日期
            day = '%02d' % last_day
            year = str(year)  # 年份
            firstDate = ''.join([year, '-', month, '-01'])  # 当前月的第一天
            lastDate = ''.join([year, '-', month, '-', day])  # 当前月的最后一天

            df_oneMonth = df[(df.index >= firstDate) & (df.index <= lastDate)]
            # 提取月初到月底之间的数据块

            if len(df_oneMonth) > 0:  # 若存在交易日（处理月份用）
                numSum += 1  # 当前月份合计递增

                firstRecoder = df_oneMonth.iloc[0]  # 月初首条记录
                lastRecoder = df_oneMonth.iloc[-1]  # 月末最后一条记录

                firstClose = firstRecoder['close']  # 月初的收盘价
                lastClose = lastRecoder['close']  # 月末的收盘价

                if firstClose < lastClose:  # 比较月初月末收盘价，判断涨跌
                    numInc += 1
                else:
                    numDec += 1

    except IOError:
        print('CSV文件不存在，跳过', filename)
        pass  # 跳过，不处理

    # print('numSum,numInc,numDec = ', numSum, numInc, numDec)
    return numSum, numInc, numDec  # 返回值为当前月份合计，上涨月份，下跌月份合计


def zw_stk_anz_m01(myZwDatX, indexFile, path, month):
    """
    针对当前月份，对股票索引文件中的每只股票进行上涨或下跌的统计，数据保存为字典格式返回
    :param myZwDatX: zwDatX类实例
    :param indexFile: 股票索引名称
    :param path: 数据文件存放的目录 './zwDat/cn/xday/'
    :param month: 指定的当前月份
    :return: monTotal 包含指定月份的统计数据的字典
    """
    filename = myZwDatX.rdatInx + indexFile + ".csv"  # filename = ./zwDat/inx/inx_code.csv

    codeType = 'gbk'  # 应该统一使用utf-8编码格式
    if 'us' in path:
        codeType = 'utf-8'
    # print('文件路径 文件编码：', filename, codeType)

    df = pd.read_csv(filename, encoding=codeType)  # 读取csv数据文件

    # print(df.head())
    # print('文件路径：',filename)

    monTotal = dict()
    monTotal['inxFile'] = indexFile  # 股票索引名称
    monTotal['month'] = month  # 月份 01~12
    monTotal['numSum'] = 0  # 当前月总数合计
    monTotal['numInc'] = 0  # 上涨数合计
    monTotal['numDec'] = 0  # 下跌数合计

    numStk = len(df['code'])
    monTotal['numStk'] = numStk  # 股票总支数

    for i, stkCode in enumerate(df['code']):  # 遍历当前类别的股票代码
        if not isinstance(stkCode, str):  # 非正常股票代码处理
            stkCode = "%06d" % stkCode

        # print(stkCode, path, month)
        stkMonSum, stkMonAdd, stkMonDec = zw_anz_m1sub(stkCode, path, month)
        # 一支股票在当前月份内的总的、上涨、下跌合计

        monTotal['numSum'] = monTotal['numSum'] + stkMonSum
        monTotal['numInc'] = monTotal['numInc'] + stkMonAdd
        monTotal['numDec'] = monTotal['numDec'] + stkMonDec
        # print(i, '/', numStk, stkCode, monTotal)

    monTotal['preInc'] = np.round(monTotal['numInc'] * 100 / monTotal['numSum'])  # 上涨百分比
    monTotal['preDec'] = np.round(monTotal['numDec'] * 100 / monTotal['numSum'])  # 下跌百分比

    # print(monTotal)
    return monTotal  # dict格式


def zw_stk_anz_mx(myZwDatX, indexFile, path):
    """
    按每个股票索引文件，生成相应的csv文件
    :param myZwDatX: zwDatX类的实例
    :param indexFile: 股票索引文件名，用于输出csv文件名
    :param path: 相应的csv数据文件存放的目录 例如'./zwDat/cn/xday/'
    :return: 空
    """
    columns = [  # 构造csv文件的字段名
        'inxFile'  # 股票索引名称
        , 'month'  # 当前月份
        , 'numStk'  # 当前索引股票总支数
        , 'numSum'  # 当前月份合计
        , 'numInc'  # 上涨月份合计
        , 'numDec'  # 下跌月份合计
        , 'preInc'  # 上涨百分比
        , 'preDec'  # 下跌百分比
    ]

    df = pd.DataFrame(columns=columns)  # 定义dataframe
    filename = "temp/monTotal_" + indexFile + ".csv"  # 将要保存csv文件的路径
    # print('csv文件的路径: ' + filename)

    for i in range(12):  # 遍历1～12月
        month = "%02d" % (i + 1)  # 两位表示的月份

        monTotal = zw_stk_anz_m01(myZwDatX, indexFile, path, month)
        # 当前股票类别、当前月的涨跌统计 字典格式

        ds = pd.Series(monTotal, index=columns)  # 将字典内容转成一列数据
        ds = ds.T  # 将列数据转成行数据
        df = df.append(ds, ignore_index=True)  # 将行数据添加到dataframe中

        # break  # 测试用
    # print(df.head())

    if not os.path.exists('temp'):
        os.mkdir('temp')
    df.to_csv(filename, index=False, encoding='utf-8')  # 将dataframe数据存盘csv
    print('已完成文件', filename)


def zw_stk_anz_mx_all(myZwDatX, indexList):
    """
    遍历股票indexList中的股票，选择相应的数据访问路径，调用zw_stk_anz_mx函数
    :param myZwDatX: zwDatX类的实例，用于获取设置参数
    :param indexList: 股票索引列表
    :return: 空
    """
    for indexFile in indexList:
        if 'Yah' in indexFile:
            path = myZwDatX.rdat + 'us/Day/'  # path = ./zwDat/us/day/
        elif indexFile == 'inx_code':
            path = myZwDatX.rdat + 'cn/xday/'  # path = ./zwDat/cn/xday/ 指数数据
        elif 'stk' in indexFile:
            path = myZwDatX.rdat + 'cn/Day/'  # path = ./zwDat/cn/day/ 个股数据
        else:
            path = '查无此处'

        # print('indexFile path = ', indexFile, path)
        zw_stk_anz_mx(myZwDatX, indexFile, path)  # 生成csv文件


def main():
    """
    主控模块
    :return: 空
    """
    root = './zwDat/'
    myZwDatX = zw.zwDatX(root)  # 用数据文件根目录实例化zwDatX类

    # 相应的美国股市数据文件还没有下载，先注释掉以下代码
    usList = [
        'inxYahoo30sp'  # 道琼斯30指数美股代码
        , 'inxYahoo100ns'  # 纳斯达克100指数美股代码
        , 'inxYahoo100sp'  # 道琼斯100工业指数美股代码
        , 'inxYahoo600'  # 量化常用美股600股票代码
        , 'inxYahoo500sp'  # 道琼斯500指数美股代码
        , 'inxYahoo'  # 全部6688美股代码
    ]
    zw_stk_anz_mx_all(myZwDatX, usList)

    # cnList = [
    #     'inx_code'  # 中国A股大盘及各种指数代码
    #     , 'stk_sz50'  # 中国上证50指数股票代码
    #     , 'stk_hs300'  # 中国沪深300指数股票代码
    #     , 'stk_zz500'  # 中国中证500指数股票代码
    #     , 'stk_code'  # 中国A股2810只股票代码
    # ]
    # zw_stk_anz_mx_all(myZwDatX, cnList)

    print('全部处理完成')


if __name__ == '__main__':
    main()

