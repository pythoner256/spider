# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TentcentSpiderItem(scrapy.Item):
    position_url = scrapy.Field()  # 职位链接
    position_name = scrapy.Field()  # 职位名称
    position_category = scrapy.Field()  # 职位类别
    number = scrapy.Field()  # 招聘人数
    date = scrapy.Field()  # 招聘时间


