#!/usr/bin/python
#encoding=utf8

import sys
import time
import tushare as ts

sys.path.append('../common')
from log import logger
from db_wrapper import DBWrapperFactory

db_to_ts = {
        'c_price' : 'price',
        'c_pchange' : 'pchange',
        'c_change' : 'change',
        'c_volume' : 'volume',
        'c_amount' : 'amount',
        'c_type' : 'type',
        }

def compose_time(v_time):
    return '%s %s' % (time.strftime("%Y-%m-%d", time.localtime()), v_time)

def save_to_db(df, stock_code):
    if df is None:
        return

    sql = 'insert into t_stock_tick_info (' + ','.join(db_to_ts.keys()) \
          + ', c_date_time, c_code, c_create_time) values'

    for index, row in df.iterrows():
        sql += '(' + ','.join("'%s'" % row[column] for column in db_to_ts.values()) \
               + ", '%s'" % compose_time(row['time'])+ ", '%s'" % stock_code + ", now()),"

    sql = sql[:-1]
    sql += 'ON DUPLICATE KEY UPDATE '
    for column in db_to_ts.keys():
        sql += '%s = VALUES(%s),' % (column, column)
    sql = sql[:-1]

    DBWrapperFactory.get_instance('d_finance').execute_sql(sql)

def local_main():
    if len(sys.argv) != 2:
        print sys.argv[0], "[stock id]"
        return

    stock_code = sys.argv[1]
    for i in xrange(5):
        df = ts.get_today_ticks(stock_code)
        if df is not None:
            break

    if df is None:
        logger.error("request error")
        return

    save_to_db(df, stock_code)

if __name__ == '__main__':
    local_main()
