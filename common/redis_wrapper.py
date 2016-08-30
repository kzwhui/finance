#!/usr/bin/python
#encoding=utf8

import sys
import redis
sys.path.append('../conf')
from conf import g_conf
sys.path.append('../common')
from log import logger

class CRedisWrapper(object):
    def __init__(self, conf = None):
        self.pool = None
        self.get_redis_pool(conf)
        self.r = None

    def get_redis_pool(self, config = None):
        if not config: 
            config = g_conf.REDIS_CONF 

        addr = config.get('addr')
        ip = addr['ip']
        port = addr['port']
        logger.info("ip=%s, port=%s" % (ip, port))
        pool = redis.ConnectionPool(host=ip, port=port)  
        return pool

    def get_redis(self):
        if self.r:
            return self.r

        if not self.pool:
            self.pool = self.get_redis_pool()

        if not self.pool:
            logger.error("no redis pool")
            return None
        self.r = redis.Redis(connection_pool=self.pool)
        return self.r

    def set_value(self, key, value, ttl=None):
        r = self.get_redis()
        if not r:
            logger.error("no redis connected")
            return "no redis error"
        if not ttl:
            return r.set(key, value)
        else:
            return r.setex(name=key, time=ttl, value=value)

    def get_value(self, key):
        r = self.get_redis()
        if not r:
            logger.error("no redis connected")
            return "no redis connected"
        return r.get(key)

    def del_key(self, key):
        r = self.get_redis()
        if not r:
            logger.error("no redis connected")
            return "no redis connected"
        return r.delete(key)

def test():
    key = "hellow"
    value = "test"
    r = CRedisWrapper()
    r.set_value(key, value) 
    v = r.get_value(key) 
    print "k=%s, v=%s" % (key, v)

def main():
    test()

if __name__ == "__main__":
    main()

