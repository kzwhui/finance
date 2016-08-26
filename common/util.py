#!/usr/bin/python
#encoding=utf8

'''
常用的函数
'''

import sys
import json
import xlwt
from log import logger

# 由于脚本编码的方式均为ut8，那么默认进来的数据均为utf8格式
def data2xls(data, xlsname, sheet_name = 'sheet1'):
    if not data or not xlsname:
        logger.error('data or xlsname filename is empty')
        return

    xls=xlwt.Workbook()
    # xls要求传进来的数据未unicode字符
    sheet = xls.add_sheet(sheet_name.decode('utf8'), cell_overwrite_ok=True)
    for i in xrange(len(data)):
        for j in xrange(len(data[i])):
            sheet.write(i, j, ('%s' % data[i][j]).decode('utf8'))

    xls.save(xlsname + '.xls')
    logger.info('suc to create %s' % xlsname)

def dict_to_readable_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False, encoding="utf8")

def dict_to_short_json(data):
    return json.dumps(data, ensure_ascii=False, encoding='utf8')


############################################################
def do_test():
    data = [
        ['测试', 5, '上班'],
        [6, '创意'],
        ['涨', '不涨', '跪了', 1999]
    ]

    data2xls(data, 'test.xls', '测试')

    dict_data = {
            1 : 'abc',
            'abc' : "哈喽"
            }
    print dict_data
    print dict_to_readable_json(dict_data)
    print dict_to_short_json(dict_data)

if __name__ == '__main__':
    do_test()
