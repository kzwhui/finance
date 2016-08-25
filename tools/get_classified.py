#!/usr/bin/python
#encoding=utf8

import sys
import tushare as ts
from pandas import ExcelWriter

def local_main():
    writer = ExcelWriter('classify.xlsx')

    df = ts.get_industry_classified()
    if df is not None:
        df.to_excel(writer, sheet_name = u'行业')

    df = ts.get_concept_classified()
    if df is not None:
        df.to_excel(writer, sheet_name = u'概念')

    df = ts.get_area_classified()
    if df is not None:
        df.to_excel(writer, sheet_name = u'地域')

    df = ts.get_sme_classified()
    if df is not None:
        df.to_excel(writer, sheet_name = u'中小板')

    df = ts.get_gem_classified()
    if df is not None:
        df.to_excel(writer, sheet_name = u'创业板')

    df = ts.get_hs300s()
    if df is not None:
        df.to_excel(writer, sheet_name = 'hs300s')

    df = ts.get_sz50s()
    if df is not None:
        df.to_excel(writer, sheet_name = 'sz50s')

    df = ts.get_zz500s()
    if df is not None:
        df.to_excel(writer, sheet_name = 'zz500s')

    writer.save()

if __name__ == '__main__':
    local_main()
