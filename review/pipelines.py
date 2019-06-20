# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import ReviewItem, CommentItem
from scrapy.item import Item
from .settings import REDIS_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_USERNAME, MONGODB_PASSWORD
import pymongo


class ReviewPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(REDIS_HOST, MONGODB_PORT)
        db = client['spider']
        if db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD):
            self.collect = db[MONGODB_DB]
            self.collect2 = db['comment']

    def open_spider(self, spider):
        pass

    def process_item(self, item: Item, spider):
        item['title'] = item['title'].split()[0]
        if isinstance(item, CommentItem):
            self.collect2.insert_one(dict(item))
        elif isinstance(item, ReviewItem):
            if item.get('num', None):
                item['num'] = int(item['num'].split('.')[1])
                item['actor'] = ''.join(item['actor'].split())
            data = dict(item)
            self.collect.find_one_and_update({'title': item['title']}, {'$set': data}, upsert=True)
        return item

    def close_spider(self, spider):
        # self.collect.close()
        pass
