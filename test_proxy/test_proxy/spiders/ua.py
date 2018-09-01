# -*- coding: utf-8 -*-
import scrapy


class UaSpider(scrapy.Spider):
    name = 'ua'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        self.logger.debug(response.text)
