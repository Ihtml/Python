# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def start_requests(self):
        # 建立浏览器对象 ，通过Phantomjs
        browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
        # 设置访问的url
        url = 'https://www.zhihu.com/signin'
        # 访问url
        browser.get(url)
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "13012345678")

        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "password")

        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton").click()

    def parse(self, response):
        pass
