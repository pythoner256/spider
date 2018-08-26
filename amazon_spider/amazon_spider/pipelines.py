# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from amazon_spider.settings import mongo_collection, mongo_db, mongo_port, mongo_host


class AmazonSpiderPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        db = mongo_db
        collection = mongo_collection
        client = pymongo.MongoClient(host=host, port=port)
        amazon_db = client[db]
        amazon_collection = amazon_db[collection]
        self.export = amazon_collection

    def process_item(self, item, spider):
        data = dict(item)
        self.export.insert(data)
        return item
