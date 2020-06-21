# -*- coding: utf-8 -*-
import scrapy
from pytz import timezone
from datetime import datetime as dt
from scrapy_myproduct.items import RakutenItem
import logging

# debug code
# scrapy shell https://search.rakuten.co.jp/search/mall/%E3%83%9E%E3%82%B9%E3%82%AF/101070
# response.xpath('//div[@class="dui-card searchresultitem"]')[0].xpath('div[@class="content merchant _ellipsis"]/a/text()').extract()
# stop debug 'ctrl+D'

class RakutenSpider(scrapy.Spider):
    name = 'rakuten'
    allowed_domains = ['rakuten.co.jp']

    # scrapy crawl rakuten -a seller='UNICONA' -a keyword='マスク' -a category_code='101070' -o mask_202006211717.csv
    def __init__(self, seller='', keyword='', category_code='', *args, **kwargs):
        super(RakutenSpider, self).__init__(*args, **kwargs)
        self.seller = seller
        self.keyword = keyword
        self.category_code = category_code
        self.start_urls = ['https://search.rakuten.co.jp/search/mall/' + self.keyword + '/' + self.category_code]


    def parse(self, response):

        logger = logging.getLogger()

        for item in response.xpath('//div[@class="dui-card searchresultitem"]'):

            #販売者に含まれているタグ指定
            str_seller = item.xpath('div[@class="content merchant _ellipsis"]/a/text()').extract_first()

            if self.seller in str_seller:

                # logger.warning(str_seller)

                now = dt.now(timezone('Asia/Tokyo'))
                date = now.strftime('%Y-%m-%d')
                jst_time = now.strftime('%Y-%m-%dT%H-%M-%S')

                logger.warning(jst_time)

                product = RakutenItem()

                #タイトル
                product['title'] = item.xpath('div[@class="content title"]/h2/a/@title').extract_first()
                #キーワード
                product['keyword'] = self.keyword
                #商品URL
                product['item_url'] = item.xpath('div[@class="content title"]/h2/a/@href').extract_first()
                #ページ数
                product['page_num'] = response.xpath('//div[@class="dui-container pagination _centered"]/div[@class="dui-pagination"]/a[@class="item -active currentPage"]/text()').extract()

                #ページURL
                product['page_url'] = response.url
                #販売者
                product['seller'] = str_seller

                #データ取得時刻
                product['search_time'] = jst_time

                yield product

        next_page = response.xpath('//div[@class="dui-container pagination _centered"]/div[@class="dui-pagination"]/a[@class="item -next nextPage"]/@href')

        if next_page:
            # 楽天は150ページまである。
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse)
        else:
            pass
        # pass
