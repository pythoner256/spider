# -*- coding: utf-8 -*-
import scrapy
from amazon_spider.items import AmazonSpiderItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn']
    start_url = 'https://www.amazon.cn/%E5%AE%B6%E5%B1%85%E7%94%A8%E5%93%81/b/ref=topnav_storetab_hg?ie=UTF8&node=831780051'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_index)

    def parse_index(self, response):
        link_list = response.xpath("//div[@class='a-row a-spacing-mini']//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']/@href").extract()
        for goods_url in link_list:
            yield scrapy.Request(goods_url, callback=self.parse)
        pre_link = "https://www.amazon.cn"
        try:
            next_link = response.xpath("//a[@id='pagnNextLink']/@href").extract_first()
            next_link = pre_link + next_link
        except Exception:
            pass
        else:
            yield scrapy.Request(next_link, callback=self.parse_index)

    def parse(self, response):
        item = AmazonSpiderItem()
        item['goods_name'] = response.xpath("//span[@id='productTitle']/text()").extract_first().strip()
        # 商品存在秒杀价
        try:
            discout_price = response.xpath("//span[@id='priceblock_dealprice']/text()")
            section_price = response.xpath("//span[@id='priceblock_ourprice']/text()")
            if discout_price:
                item['price'] = discout_price.extract_first().strip()
            elif section_price:
                item['price'] = section_price.extract_first().strip()
            else:
                item['price'] = response.xpath("//span[@class='a-color-price']/text()").extract_first().strip()
        except Exception:
            pass
        item['shop_name'] = response.xpath("//a[@id='bylineInfo']/text()").extract_first().strip()
        yield item

