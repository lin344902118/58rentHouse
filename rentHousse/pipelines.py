# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs


class RenthoussePipeline(object):
    def __init__(self):
        self.file = codecs.open('58rent.csv', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        datas = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(datas)
        return item

    def spider_closed(self, spider):
        self.file.close()
