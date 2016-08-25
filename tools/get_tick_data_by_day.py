#!/usr/bin/python
#encoding=utf8

import sys
import tushare as ts
from pandas import ExcelWriter

def local_main():
    if len(sys.argv) != 3:
        print sys.argv[0], " [stock id] [date]"
        return
    
    writer = ExcelWriter(sys.argv[1] + '_%s' % sys.argv[2] + '_tick.xlsx')
    df = ts.get_tick_data(sys.argv[1], date=sys.argv[2])
    if df is not None:
        df.to_excel(writer, sheet_name = 'his')

    writer.save()

if __name__ == '__main__':
    local_main()
