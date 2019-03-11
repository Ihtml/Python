# -*- coding: utf-8 -*-
__author__ = 'ife'
__date__ = '2019-03-11 23:15'

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5("http://img2.imgtn.bdimg.com/it/u=1883701644,1651591262&fm=26&gp=0.jpg".encode("utf-8")))
