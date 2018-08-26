# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    goods_name = scrapy.Field()
    price = scrapy.Field()
    shop_name = scrapy.Field()
