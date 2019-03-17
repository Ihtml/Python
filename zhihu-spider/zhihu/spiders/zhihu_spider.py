# -*- coding: utf-8 -*-
import scrapy
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from mouse import move, click


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    def start_requests(self):
        import pickle
        cookies = pickle.load(open("/Users/github/Python/zhihu-spider/cookies/zhihu_cookie", "rb"))
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]
        print(cookie_dict)
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

        # 手动启动本地Chrome
        # from selenium.webdriver.chrome.options import Options
        #
        # chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 建立浏览器对象
        # browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",
        #                            chrome_options=chrome_options)
        # # 设置访问的url
        # url = 'https://www.zhihu.com/signin'
        # # 访问url
        # browser.get(url)
        # time.sleep(3)
        # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL, "a")
        # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
        #     "18612345678")
        # time.sleep(3)
        # browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL, "a")
        # browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
        #     "123456")
        # time.sleep(3)
        # # move(900, 600)
        # # click()
        #
        # browser.find_element_by_css_selector(
        #     ".Button.SignFlow-submitButton").click()

        # browser.get("https://www.zhihu.com")
        # cookies = browser.get_cookies()
        # import pickle
        # # 将对象放到文件当中
        # pickle.dump(cookies, open("/Users/github/Python/zhihu-spider/cookies/zhihu_cookie", "wb"))
        # cookie_dict = {}
        # for cookie in cookies:
        #     cookie_dict[cookie["name"]] = cookie["value"]
        # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

        # time.sleep(30)

    def parse(self, response):
        pass
