#!/usr/bin/python
#encoding=utf8

import sys
import time
from sqlalchemy import create_engine
import tushare as ts

sys.path.append('../common')
from log import logger
from db_wrapper import DBWrapperFactory

def get_db_key(key):
    return 'c_%s' % key

def save_to_db(df):
    if df is None:
        return

    columns = [column for column in df.columns]
    extra_key = ['date', 'time']
    db_key = set(columns) - set(extra_key)
    sql = 'insert into t_real_time_info (' + ','.join(get_db_key(key) for key in db_key) \
          + ', c_date_time, c_create_time) values'

    for index, row in df.iterrows():
        sql += '(' + ','.join("'%s'" % row[column] for column in db_key) \
               + ", '" + row['date'] + " " + row['time'] + "', now()),"
    sql = sql[:-1]
    DBWrapperFactory.get_instance('d_finance').execute_sql(sql)

def local_main():
    if len(sys.argv) != 2:
        print sys.argv[0], " [stock id[,stock id[...]]]"
        return

    ids_string = sys.argv[1]
    stock_ids = ids_string.split(',')
    for i in xrange(5):
        df = ts.get_realtime_quotes(stock_ids)
        if df is not None:
            break

    if df is None:
        logger.error("request error")
        return

    save_to_db(df)

if __name__ == '__main__':
    local_main()