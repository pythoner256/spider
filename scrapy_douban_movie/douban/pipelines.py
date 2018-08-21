# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from douban.settings import mongo_host, mongo_port, mongo_db, mongo_collection


class DoubanPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        db = mongo_db
        coll = mongo_collection
        client = pymongo.MongoClient(host=host, port=port)
        my_db = client[db]
        self.post = my_db[coll]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
