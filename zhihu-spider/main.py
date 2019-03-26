# -*- coding: utf-8 -*-
__author__ = 'ife'
__date__ = '2019-03-16 22:14'

from scrapy.cmdline import execute

import sys
import os

# 获取文件所在父目录的路径
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "zhihu_spider"])
