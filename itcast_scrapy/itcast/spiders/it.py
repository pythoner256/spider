# -*- coding: utf-8 -*-
import scrapy
from itcast.items import ItcastItem


class ItSpider(scrapy.Spider):
    name = 'it'
    allowed_domains = ['itcast.cn']

    def start_requests(self):
        start_urls = [
            "http://www.itcast.cn/channel/teacher.shtml#aandroid",
            "http://www.itcast.cn/channel/teacher.shtml#ac",
            "http://www.itcast.cn/channel/teacher.shtml#acloud",
            "http://www.itcast.cn/channel/teacher.shtml#aios",
            "http://www.itcast.cn/channel/teacher.shtml#ajavaee",
            "http://www.itcast.cn/channel/teacher.shtml#anetmarket",
            "http://www.itcast.cn/channel/teacher.shtml#aphp",
            "http://www.itcast.cn/channel/teacher.shtml#apython",
            "http://www.itcast.cn/channel/teacher.shtml#astack",
            "http://www.itcast.cn/channel/teacher.shtml#aui",
            "http://www.itcast.cn/channel/teacher.shtml#aweb"
        ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = response.xpath("//div[@class='li_txt']")
        item = ItcastItem()
        for each in items:

            name = each.xpath("./h3/text()").extract_first()
            title = each.xpath("./h4/text()").extract_first()
            info = each.xpath("./p/text()").extract_first()

            item['name'] = name
            item['title'] = title
            item['info'] = info

            yield item


