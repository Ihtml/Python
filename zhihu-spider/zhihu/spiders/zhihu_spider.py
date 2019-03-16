# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def start_requests(self):
        # 手动启动本地Chrome
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 建立浏览器对象 ，通过Phantomjs
        browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",
                                   chrome_options=chrome_options)
        # 设置访问的url
        url = 'https://www.zhihu.com/signin'
        # 访问url
        browser.get(url)
        time.sleep(5)
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL, "a")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "13012345678")
        time.sleep(5)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL, "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "password")
        time.sleep(5)
        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton").click()
        time.sleep(30)

    def parse(self, response):
        pass
