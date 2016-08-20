#!/usr/bin/python
#encoding=utf8
# just for study crawler, by zwh
# this will crawl top 250 of book of douban in detail
# url: https://book.douban.com/top250

#CREATE TABLE `t_book_info` (
#  `c_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#  `c_book_title` varchar(256) NOT NULL,
#  `c_book_url` varchar(512) NOT NULL,
#  `c_publish_time` varchar(32) NOT NULL,
#  `c_writer` varchar(512) NOT NULL,
#  `c_price` float NOT NULL,
#  `c_douban_id` varchar(64) NOT NULL,
#  `c_score` float NOT NULL,
#  `c_description` text NOT NULL,
#  `c_modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#  `c_create_time` datetime NOT NULL,
#  PRIMARY KEY (`c_id`),
#  UNIQUE KEY `douban_id` (`c_douban_id`),
#  KEY `book_title` (`c_book_title`),
#  KEY `modify_time` (`c_modify_time`),
#  KEY `create_time` (`c_create_time`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8

import sys
import re
import requests
import MySQLdb
from bs4 import BeautifulSoup as BS
from urlparse import urljoin
sys.path.append('../common')
sys.path.append('../conf')
from db_wrapper import DBWrapperFactory
from log import logger
from conf import g_conf

class TopBookCrawler:
    T_KEYS = ['c_book_title', 'c_book_url', 'c_publish_time', 'c_writer', 'c_price', 'c_douban_id', 'c_score', 'c_description']

    def __init__(self, url):
        self.count = 0
        self.base = url
        self.top_book_list = []
        self.db_wrapper = DBWrapperFactory.get_instance('d_crawler_info')

    def run(self):
        logger.info("crawler start")
        start_num = 0
        post_url = '/top250?start=%s' % start_num
        url = urljoin(self.base, post_url)
        self.get_page_book_list(url)

    def get_page_book_list(self, url):
        try:
            resp = requests.get(url, timeout = 3)
        except requests.exceptions.RequestException, e:
            logger.error("request error: %s" % e)
            return

        soup = BS(resp.content, 'html.parser')
        item_list = soup.find_all('tr', 'item')
        logger.debug("%s items has been found" % len(item_list))
        for item in item_list:
            book_info = {}
            book_tag = item.find('a', title=re.compile('.*'))
            book_info["c_book_title"] = book_tag['title'].strip()
            if not self.get_detail_book_info(book_tag['href'], book_info):
                continue
            self.count += 1
            self.top_book_list.append(book_info)

    def get_detail_book_info(self, ready_url, book_info):
        url = urljoin(self.base, ready_url)
        logger.debug('book detail url: %s' % url)

        try:
            resp = requests.get(url, timeout = 3)
        except requests.exceptions.RequestException, e:
            logger.error("request error: %s" % e)
            return False

        soup = BS(resp.content, 'html.parser')
        item = soup.find('div', id='info')
        book_info['c_writer'] = item.find('a').string.strip()

        text_list = item.get_text().splitlines()
        for t in text_list:
            match_obj = re.match(r'.*\S.*:.*\S.*', t)
            if not match_obj:
               continue
            tmp_list = t.split(':')
            if len(tmp_list) != 2:
                continue
            if tmp_list[0].encode('utf-8') == '出版年':
                book_info['c_publish_time'] = tmp_list[1].strip()
            if tmp_list[0].encode('utf-8') == '定价':
                number_obj = re.search(r'\d\d*', tmp_list[1])
                book_info['c_price'] = number_obj.group() if number_obj else ''

        book_info['c_book_url'] = url

        match_obj = re.search(r'\d\d*', url)
        book_info['c_douban_id'] = match_obj.group() if match_obj else ""
        book_info['c_score'] = soup.find('strong', 'll rating_num ').string.strip()
        book_info['c_description'] = soup.find('div', 'intro').find('p').string.strip()
        logger.debug('book info = %s' % book_info)

        return True

    def get_top_book_list(self):
        return self.top_book_list

    def dump_to_terminal(self):
        for book in self.top_book_list:
            print book['c_book_title']

    def dump_to_file(self, filename):
        fd = open(filename, 'w')
        for book in self.top_book_list:
            fd.write('%s\n' % book['c_book_title'].encode('utf-8'))
        fd.close()

    def dump_to_mysql(self):
        if not self.top_book_list:
            return

        sql = "insert into t_book_info ("
        for key in self.T_KEYS:
            sql += key + ','
        sql += 'c_create_time) values'

        for book in self.top_book_list:
            sql += "("
            for key in self.T_KEYS:
                sql += "'%s'," % book.get(key, '').encode('utf-8')
            sql += 'now()),'

        sql = sql[:-1]
        affect = self.db_wrapper.execute_sql(sql)
        logger.info("%s lines affect" % affect)

def main():
    url = 'https://book.douban.com'
    crawler = TopBookCrawler(url)
    crawler.run()
    crawler.dump_to_terminal()
    crawler.dump_to_file('top_book_list.txt')
    crawler.dump_to_mysql()

if __name__ == '__main__':
    main()
