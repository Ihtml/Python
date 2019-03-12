# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item


# 自定义管道，拿到存放图片的本地路径,重写了ImagesPipeline的item_completed方法
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path

        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')
        self.file.write('[')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.seek(-2, os.SEEK_END)  # 定位到倒数第二个字符，即最后一个逗号
        self.file.truncate()  # 删除最后一个逗号
        self.file.write(']')  # 文件末尾加入一个‘]’
        self.file.close()  # 关闭文件


class JsonExporterPipleline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


