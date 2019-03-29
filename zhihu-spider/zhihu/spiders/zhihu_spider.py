# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json

try:
    import urlparse as parse
except:
    from urllib import parse

from scrapy.loader import ItemLoader
from zhihu.items import ZhihuQuestionItem, ZhihuAnswerItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from mouse import move, click
import pyautogui


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
        # 手动启动本地Chrome
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 建立浏览器对象
        browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",
                                   chrome_options=chrome_options)
        try:
            # 窗口最大化
            browser.maximize_window()
        except:
            pass

        browser.get("https://www.zhihu.com/signin")

        # 浏览器执行js代码获取浏览器工具栏高度
        browser_navigation_panel_height = browser.execute_script('return window.outerHeight - window.innerHeight;')
        # browser_navigation_panel_height = 71

        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL, "a")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "18612345678")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL, "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "123456")
        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton").click()

        # 等待加载完成
        time.sleep(5)
        # 判断是否登录成功
        login_success = False
        while not login_success:
            try:
                # 如果能找到某个元素证明登录成功
                notify_element = browser.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
                login_success = True
            except:
                pass

            try:
                # 查询是否有英文验证码
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_element = None
            try:
                # 查询是否有中文验证码
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_element = None

            if chinese_captcha_element:
                y_relative_coord = chinese_captcha_element.location['y']
                y_absolute_coord = y_relative_coord + browser_navigation_panel_height
                x_absolute_coord = chinese_captcha_element.location['x']
                # x_absolute_coord = 842
                # y_absolute_coord = 428

                """
                保存图片
                1. 通过保存base64编码
                2. 通过crop方法
                """
                # 1. 通过保存base64编码
                base64_text = chinese_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_cn.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from zheye import zheye
                z = zheye()
                positions = z.Recognize("yzm_cn.jpeg")

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

                if len(positions) == 2:
                    # 保存到本地的图片长宽是原图的两倍
                    first_point = [int(pos_arr[0][0] / 2), int(pos_arr[0][1] / 2)]
                    second_point = [int(pos_arr[1][0] / 2), int(pos_arr[1][1] / 2)]

                    # move((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    # click()
                    #
                    # move((x_absolute_coord + second_point[0]), y_absolute_coord + second_point[1])
                    # click()
                    pyautogui.moveTo((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    pyautogui.click()

                else:
                    first_point = [int(pos_arr[0][0] / 2), int(pos_arr[0][1] / 2)]

                    # move((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    # click()
                    pyautogui.moveTo((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    pyautogui.click()

                # 输入验证码后重新登录
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "xxx")

                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                    "xxx")
                browser.find_element_by_css_selector(
                    ".Button.SignFlow-submitButton").click()
                browser.find_element_by_css_selector(
                    ".Button.SignFlow-submitButton").click()


# def start_requests(self):
#     import pickle
#     # 将文件中的cookie数据解析为一个Python对象
#     cookies = pickle.load(open("/Users/github/Python/zhihu-spider/cookies/zhihu_cookie", "rb"))
#     cookie_dict = {}
#     for cookie in cookies:
#         cookie_dict[cookie["name"]] = cookie["value"]
#     print(cookie_dict)
#     return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
#
#     # 手动启动本地Chrome
#     from selenium.webdriver.chrome.options import Options
#
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#
#     # 建立浏览器对象
#     browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",
#                                chrome_options=chrome_options)
#     # 设置访问的url
#     url = 'https://www.zhihu.com/signin'
#     # 访问url
#     browser.get(url)
#     time.sleep(3)
#     # 填写手机号和密码登录
#     browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL, "a")
#     browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
#         "18612345678")
#     time.sleep(3)
#     browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL, "a")
#     browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
#         "123456")
#     time.sleep(3)
#
#     # move(900, 600)
#     # click()
#
#     browser.find_element_by_css_selector(
#         ".Button.SignFlow-submitButton").click()
#
#     browser.get("https://www.zhihu.com")
#     cookies = browser.get_cookies()
#     import pickle
#     # 将cookie对象写到文件当中
#     pickle.dump(cookies, open("/Users/github/Python/zhihu-spider/cookies/zhihu_cookie", "wb"))
#     cookie_dict = {}
#     for cookie in cookies:
#         cookie_dict[cookie["name"]] = cookie["value"]
#     return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

    def parse(self, response):
        """
            提取出html页面中的所有url 并跟踪这些url进行一步爬取
            如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)


    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        if "QuestionHeader-title" in response.text:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-actions button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item


    def parse_answer(self, reponse):
        # 处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)
