# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RakutenItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    keyword = scrapy.Field()
    item_url = scrapy.Field()
    page_num = scrapy.Field()
    page_url = scrapy.Field()
    seller = scrapy.Field()
    search_time = scrapy.Field()

    pass
