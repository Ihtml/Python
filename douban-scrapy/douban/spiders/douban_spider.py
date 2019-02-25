# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
	# 这里是爬虫名
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口URL，扔到调度器里面去
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        # print(response.text)
        #获取首页的25条电影信息
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            # print(douban_item)
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            # yield到管道，使管道接受数据
            yield douban_item
        
        nextLink = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        # 第十页是最后一页，没有下一页得链接
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield scrapy.Request('https://movie.douban.com/top250'+nextLink, callback=self.parse)
            # 递归将下一页的地址传给这个函数自己，在进行爬取
