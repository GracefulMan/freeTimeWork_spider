# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient
from datetime import datetime
client = MongoClient()
collection = client['beike']['second_hand']
class MyspiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'beike':
            item['address']['houseInfo'] = item['address']['houseInfo'].replace(" ",'')
            item['address']['houseInfo'] = item['address']['houseInfo'].replace("\n",'')
            tag_res = []
            for tag in item['tag']:
                tag = tag.replace(" ",'')
                tag = tag.replace("\n",'')
                if len(tag)!=0 and tag not in tag_res:
                    tag_res.append(tag)
            item['tag'] = tag_res
            item['update_time'] = datetime.now().isoformat()
            collection.insert(dict(item))



