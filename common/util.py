#!/usr/bin/python
#encoding=utf8

'''
常用的函数
'''

import sys
import xlwt
from log import logger

def data2xls(data, xlsname, sheet_name = 'sheet1'):
    if not data or not xlsname:
        logger.error('data or xlsname filename is empty')
        return

    xls=xlwt.Workbook()
    sheet = xls.add_sheet(sheet_name.decode('utf8'), cell_overwrite_ok=True)
    for i in xrange(len(data)):
        for j in xrange(len(data[i])):
            sheet.write(i, j, ('%s' % data[i][j]).decode('utf8'))

    xls.save(xlsname)
    logger.info('suc to create %s' % xlsname)


############################################################
def do_test():
    data = [
        ['测试', 5, '上班'],
        [6, '创意'],
        ['涨', '不涨', '跪了', 1999]
    ]

    data2xls(data, 'test.xls', '测试')


if __name__ == '__main__':
    do_test()