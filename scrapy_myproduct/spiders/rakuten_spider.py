# -*- coding: utf-8 -*-
import scrapy


class RakutenSpiderSpider(scrapy.Spider):
    name = 'rakuten_spider'
    allowed_domains = ['rakuten.co.jp']
    start_urls = ['http://rakuten.co.jp/']

    def parse(self, response):
        pass
