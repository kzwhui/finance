#!/usr/bin/python
#encoding=utf8

import sys
import time
import tushare as ts
from pandas import ExcelWriter

def local_main():
    if len(sys.argv) != 2:
        print sys.argv[0], " [stock id]"
        return
    
    xls_name = sys.argv[1] + '_%s' % time.strftime("%Y-%m-%d", time.localtime()) + '_tick.xlsx'
    writer = ExcelWriter(xls_name)
    df = ts.get_today_ticks(sys.argv[1])
    if df is not None:
        df.to_excel(writer, sheet_name = sys.argv[1])

    writer.save()

if __name__ == '__main__':
    local_main()
