# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanMoiveSpider(scrapy.Spider):
    name = 'douban_moive'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        items = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for each in items:
            item = DoubanItem()
            item['name'] = each.xpath(".//div[@class='hd']//a/span[1]/text()").extract_first()
            item['introduce'] = each.xpath(".//div[@class='bd']//p/text()").extract_first().strip()
            item['rate'] = each.xpath(".//span[@class='rating_num']/text()").extract_first()
            item['comment'] = each.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            item['quote'] = each.xpath(".//p[@class='quote']//span/text()").extract_first()
            yield item
        links = response.xpath("//span[@class='next']//link/@href").extract()
        if links:
            url = self.start_urls[0]+links[0]
            yield scrapy.Request(url, callback=self.parse)

