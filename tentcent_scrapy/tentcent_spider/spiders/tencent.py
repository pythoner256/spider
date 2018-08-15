# -*- coding: utf-8 -*-
import scrapy
from tentcent_spider.items import TentcentSpiderItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    offset = 0
    url = "https://hr.tencent.com/position.php?keywords=Python&tid=0&lid=2218&start="

    start_urls = [url + str(offset)]

    def parse(self, response):
        items = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for each in items:
            item = TentcentSpiderItem()
            position_name = each.xpath('./td[1]/a/text()').extract_first()
            position_url = each.xpath('./td[1]/a/@href').extract_first()
            position_category = each.xpath('./td[2]/text()').extract_first()
            number = each.xpath('./td[3]/text()').extract_first()
            date = each.xpath('./td[5]/text()').extract_first()
            item['position_name'] = position_name
            item['position_url'] = position_url
            item['position_category'] = position_category
            item['number'] = number
            item['date'] = date
            yield item

        if self.offset < 320:
            self.offset += 10
        yield scrapy.Request(self.url+str(self.offset), callback=self.parse)
