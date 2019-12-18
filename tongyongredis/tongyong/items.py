# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import redis
from models.es_types import TongyongwenzhangType
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# 导入连接elasticsearch(搜索引擎)服务器方法
es=connections.create_connection(TongyongwenzhangType._doc_type.using)
redis_cli = redis.StrictRedis(host='IP地址',port=6379,db=6,password='密码')
def gen_suggets(index,info_tuple):
    #g根据字符串生成建议
    used_words=set()
    suggests=[]
    for text,weight in info_tuple:
        if text:
            #diaoyonges
            words=es.indices.analyze(index=index,body={'text':text,'analyzer':"ik_max_word"},params={"filter":["lowercase"]})
            analyzed_words=set([r["token"] for r in words["tokens"] if len(r["token"])>1] )
            news_words=analyzed_words-used_words
        else:
            news_words=set()
        if news_words:
            suggests.append({"input":list(news_words),"weight":weight})
        return  suggests
class TongyongItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    ctime = scrapy.Field()
    gtime = scrapy.Field()
    read_num = scrapy.Field()
    url = scrapy.Field()
    site_name = scrapy.Field()


    def save_to_es(self):
        article =TongyongwenzhangType()
        article.title = self['title']
        article.content = self['content']
        article.author = self['author']
        article.ctime = self['ctime']
        article.gtime = self['gtime']
        article.read_num = self['read_num']
        article.url = self['url']
        article.site_name = self['site_name']
        article.suggest = gen_suggets(TongyongwenzhangType._doc_type.index,((article.title,10),(article.content,5)))
        article.save()
        redis_cli.incr("wenzhang_count")
        return


