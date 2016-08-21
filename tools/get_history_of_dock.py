#!/usr/bin/python
#encoding=utf8

import sys
import tushare as ts

def local_main():
    if len(sys.argv) != 2:
        print sys.argv[0], " [stock id]"
        return

    stock_id = sys.argv[1]
    df = ts.get_hist_data(stock_id)
    df.to_excel(stock_id + '_his.xlsx', sheet_name = stock_id)

if __name__ == '__main__':
    local_main()