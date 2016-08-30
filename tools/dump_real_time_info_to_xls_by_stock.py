#!/usr/bin/python

import sys
import time
sys.path.append('../common')
sys.path.append('../conf')
from db_wrapper import DBWrapperFactory
from log import logger
from conf import g_conf
from util import *

def local_main():
    if len(sys.argv) != 2:
        print sys.argv[0], " [stock id]"
        return

    stock_id = sys.argv[1]
    sql = "select * from t_real_time_info where c_code = '%s' order by c_date_time" % stock_id
    rows = DBWrapperFactory.get_instance('d_finance').get_dict(sql)
    if not rows:
        print 'get no info'
        return

    xls_data = []
    title_flag = False
    for row in rows:
        if not title_flag:
            title = []
            for k in row.keys():
                title.append(k.encode('utf8'))
            xls_data.append(title)
            title_flag = True

        data = []
        for v in row.values():
            data.append(("%s" % v).encode('utf8'))
        xls_data.append(data)

    filename = stock_id + '_real_time_info'
    data2xls(xls_data, filename)

if __name__ == '__main__':
    local_main()
