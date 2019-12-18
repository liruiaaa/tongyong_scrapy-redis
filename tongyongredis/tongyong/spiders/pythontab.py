# -*- coding: utf-8 -*-
import time
import re
import redis
from urllib.parse import urljoin
from tongyong.items import TongyongItem
from scrapy.http import Request
from urllib import parse
from scrapy_redis.spiders import RedisSpider

class PythontabSpider(RedisSpider):
    name = 'pythontab'
    allowed_domains = ["pythontab.com"]
    redis_key = 'pythontab:start_urls'
    # scrapy默认处理 >=200 并且 <300 的URL，其他的会过滤掉，handle_httpstatus_list表示对返回这些状态码的URL不过滤，自己处理
    handle_httpstatus_list = [302, 400, 403, 404, 500]
    # custom_settings = {
    #     # 指定redis数据库的连接参数
    #     'REDIS_HOST': "IP地址",
    #     'REDIS_PORT': "6379",
    #     'REDIS_PARAMS': {
    #         'password': '密码',
    #         'db': 5
    #     },
    # }

    def __init__(self):
        self.start_urls=[
            'https://www.pythontab.com/html/pythonjichu/',#基础教程
            'https://www.pythontab.com/html/pythonhexinbiancheng/',#高级教程
            'https://www.pythontab.com/html/pythonweb/',#python框架
            'https://www.pythontab.com/html/hanshu/',#python函数
            'https://www.pythontab.com/html/pythongui/',#GUI教程
            'https://www.pythontab.com/html/linuxkaiyuan/',#linux教程
        ]
        self.pool = redis.StrictRedis(host='IP地址', port=6379, db=5, password='密码')
        for i in self.start_urls:
            self.pool.lpush('pythontab:start_urls',i)

    def get_start_urls(self):
        for i in self.start_urls:
            yield Request(
                url=i,
                dont_filter=True,
                callback=self.parse,
            )
    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")
        base_url=response.url

        loops=response.xpath('''//ul[@id="catlist"]//li//a/@href''').extract()
        for aurl in loops:
            post_url=urljoin(base_url,aurl)
            yield Request(
            url=post_url,
            dont_filter=True,
            callback=self.parse_detail,
        )

        next_url=response.xpath('''//a[@class="a1"][last()]//@href''').extract()[0]
        next_url=urljoin(base_url,next_url)


        if  next_url:
            yield Request(
                url=next_url,
                dont_filter=True,
                callback=self.parse,
            )

    def parse_detail(self,response):
        item = TongyongItem()
        timeArrays = time.localtime(int(time.time()))
        gtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArrays)
        item['gtime'] = gtime
        item['url'] = response.url
        item['site_name'] = 'PythonTab中文网'
        item['title'] = response.xpath('//div[@id="Article"]/h1/text()').get()
        item['read_num'] = 0
        item['ctime'] = gtime
        item['author'] = "PythonTab中文网"
        contents = response.xpath('//div[@id="Article"]//div[@class="content"]//text()').getall()
        content_text = ''.join(contents)
        content_text = re.sub(" |\t|\n|\r|\r\n", " ", content_text).strip()
        content_text = re.sub("\s+", " ", content_text).strip()
        item['content']=content_text

        return item