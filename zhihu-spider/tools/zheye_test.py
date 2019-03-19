# -*- coding: utf-8 -*-
__author__ = 'ife'
__date__ = '2019-03-19 22:53'

from zheye import zheye
z = zheye()
positions = z.Recognize('zhihu_image/a.gif')
print(positions)
