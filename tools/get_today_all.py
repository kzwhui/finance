#!/usr/bin/python
#encoding=utf8

import sys
import time
import tushare as ts
from pandas import ExcelWriter

def local_main():
    writer = ExcelWriter('%s_tick.xlsx' % time.strftime("%Y-%m-%d", time.localtime()))
    df = ts.get_today_all()
    if df is not None:
        df.to_excel(writer, sheet_name = 'ticks')
    writer.save()

if __name__ == '__main__':
    local_main()
