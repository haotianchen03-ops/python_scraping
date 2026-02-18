# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

import os
import hashlib


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item.get('url')
        if url:
            # 带上 Referer，避免 403
            yield scrapy.Request(
                url,
                headers={
                    "Referer": "https://image.baidu.com/",
                    "User-Agent": "Mozilla/5.0"
                }
            )

    # 生成“合法且稳定”的文件名：sha1(url) + 原扩展名
    def file_path(self, request, response=None, info=None, *, item=None):
        url = request.url
        # 去掉查询串，保留扩展名
        basename = url.split('?')[0]
        ext = os.path.splitext(basename)[1] or '.jpg'
        guid = hashlib.sha1(url.encode('utf-8')).hexdigest()
        return f'{guid}{ext}'

    def item_completed(self, results, item, info):
        # 有至少一张下成功就放行；否则丢弃（或改为直接返回以便仍入库）
        if not any(ok for ok, _ in results):
            raise DropItem('Image Downloaded Failed')
        return item



class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.db = None
        self.client = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.update_one({'description': item['description']}, {'$set': item}, upsert=True)
        return item

    def close_spider(self, spider):
        self.client.close()
