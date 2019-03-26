# -*- coding: utf-8 -*-
__author__ = 'ife'
__date__ = '2019-03-19 22:53'

from zheye import zheye

z = zheye()
positions = z.Recognize('zhihu_image/a.gif')

pos_arr = []
if len(positions) == 2:
    if positions[0][1] > positions[1][1]:
        pos_arr.append([positions[1][1], positions[1][0]])
        pos_arr.append([positions[0][1], positions[0][0]])
    else:
        pos_arr.append([positions[0][1], positions[0][0]])
        pos_arr.append([positions[1][1], positions[1][0]])
else:
    pos_arr.append([positions[0][1], positions[0][0]])


print(positions)
# [(50.67002741287038, 39.79313742494575), (47.541710106439055, 278.1610917745603)]
print(pos_arr)
# 从左到右第一个元素的x,y坐标，第2个元素的x,y坐标
# [[39.79313742494575, 50.67002741287038], [278.1610917745603, 47.541710106439055]]
