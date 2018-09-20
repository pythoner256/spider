# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qiushi.items import QiushiItem


class QsSpider(CrawlSpider):
    name = 'qs'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/8hr/page/1/']

    rules = (
        Rule(LinkExtractor(allow=r'page/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for each in response.xpath("//div[contains(@class,'untagged')]"):
            item = QiushiItem()
            name = each.xpath("./div[@class='author clearfix']/a[2]")
            anonymous = each.xpath("./div[@class='author clearfix']/span[2]")
            if name:  # 存在匿名用户，分别处理
                item['name'] = name.xpath("./h2/text()").extract_first().strip()
            elif anonymous:
                item['name'] = anonymous.xpath("./h2/text()").extract_first()
            item['content'] = each.xpath("./a//span/text()").extract_first().strip()
            item['num'] = each.xpath("./div[@class='stats']/span/i/text()").extract_first().strip()

            yield item


