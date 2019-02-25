# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os

class DoubanPipeline(object):
     # 构造方法，在调用类的时候只执行一次
    def __init__(self):
        super().__init__()  # 执行父类的构造方法
        self.fp = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')
        self.fp.write('[')
    # 来一个item就会调用一次这个方法

    def process_item(self, item, spider):
        # 将item转为字典
        d = dict(item)
        # 将字典转为json格式
        string = json.dumps(d, ensure_ascii=False)
        self.fp.write(string + ',\n')  # 每行数据之后加入逗号和换行
        return item

    def close_spider(self, spider):
        self.fp.seek(-2, os.SEEK_END)  # 定位到倒数第二个字符，即最后一个逗号
        self.fp.truncate()  # 删除最后一个逗号
        self.fp.write(']')  # 文件末尾加入一个‘]’
        self.fp.close()   # 关闭文件
