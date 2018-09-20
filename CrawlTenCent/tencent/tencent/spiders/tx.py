# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencent.items import TencentItem


class TxSpider(CrawlSpider):
    name = 'tx'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=30#a']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = TencentItem()
            item['positionName'] = each.xpath('./td[1]/a/text()').extract_first()
            item['positionLink'] = each.xpath('./td[1]/a/@href').extract_first()
            item['positionType'] = each.xpath('./td[2]/text()').extract_first()
            item['peopleNum'] = each.xpath('./td[3]/text()').extract_first()
            item['workLocation'] = each.xpath('./td[4]/text()').extract_first()
            item['publishTime'] = each.xpath('./td[5]/text()').extract_first()
            yield item

