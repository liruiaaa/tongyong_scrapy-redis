# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
from models.es_types import TongyongwenzhangType
# class tongyongPipeline(object):
#     def process_item(self, item, spider):
#         return item

# 异步mysql
class MysqlTwistedPipeline(object):
    def __init__(self):
        self.dbparams = {
            'host': 'IP地址',
            'user': 'root',
            'password': '密码',
            'port': 3306,
            'database': 'test',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **self.dbparams)
        self.sql = 'insert into jianshu_all_writings(title, author, content, pub_time, like_num, read_num) values(%s, %s, %s, %s, %s, %s)'

    def process_item(self, item, spider):
        result = self.dbpool.runInteraction(self.insert_data, item)
        result.addCallback(self.handle_error, item, spider)

    def insert_data(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['author'], item['content'], item['pub_time'], item['like_num'], item['read_num']))

    def handle_error(self, error, item, spider):
        print('*'*30)
        print(error)
#写入es
class EsserachPipeline(object):
    def process_item(self, item, spider):
        item.save_to_es()

        return item
