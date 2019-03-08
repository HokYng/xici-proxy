# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from .settings import HOST, PORT, DATABASE, PASSWORD, USERNAME

class ProxyPipeline(object):
    def open_spider(self):
        client = pymongo.MongoClient(HOST, PORT)
        self.db = client[DATABASE]
        self.db.authenticate(USERNAME, PASSWORD)
        self.coll = self.db['proxy']
        if 'proxy' in self.db.collection_names():
            self.coll.delete_many({})

    def process_item(self, item, spider):
        # self.coll.insert(item['proxy'])
        self.coll.insert(dict(item))
        return item

    def close_spider(self, item, spider):
        self.coll.close()

