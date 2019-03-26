# -*- coding: utf-8 -*-
import scrapy
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def getlist(name):
    with open(name + '.txt', 'r') as f:
        list = []
        for line in f.readlines():
            item = line.strip() # 把末尾的'\n'删掉
            list.append(item)
    f.close()
    return list

# 写入文件
def writetofile(list, filename):
    with open(filename + '.txt', 'w') as f:
        for item in list:
            f.write(item + '\n')
    f.close()

a = getlist("ean")
b = getlist("b") # 价格
c = getlist("c") # 网址
d = getlist("d") # 姓名

class Find2SpiderSpider(scrapy.Spider):
    name = 'find2_spider'
    allowed_domains = ['uae.souq.com']
    start_urls = ['https://uae.souq.com/ae-en/']

    def start_requests(self):
         # 建立浏览器对象
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_options.add_experimental_option("prefs",prefs)
        browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)

        price_list = []
        url_list = []
        seller_list = []

        modifiy_list = []
        for i in range(0, len(c)):
            # if d[i] != "ctss1897" and d[i] != "seventeeeeeeen":
            if i < len(c) + 1:
                print("----------------------begin-----------------------")
                print("seller index is :==================", i)
                # print("dontknow seller:===============", d[i])
                try:
                    url = c[i]
                    browser.get(url)
                    browser.find_element_by_css_selector(".other-sellers-container  .show-for-medium.bold-text").click()
                    time.sleep(0.5)
                    prices = browser.find_elements_by_css_selector("#condition-all .field.price-field")
                    names = browser.find_elements_by_css_selector("#condition-all .field.seller-name span a")
                except Exception as e:
                    b[i] = '0'
                    d[i] = 'dontknow'
                    modifiy_list.append(i+1)
                    continue
              
                name_list = []
                price_list = []
                for p in prices:
                    price = p.get_attribute('textContent')
                    price_list.append(price)
                print('价格数============', len(prices))

                print('名字数：===========', len(names))
                for j in range(0, len(names)):
                    name= names[j]
                    name = name.get_attribute('textContent')
                    print('name: ========', name)
                    name_list.append(name)
                # print('name list is :' name_list)

                print('------------info---------------')
                print('第几项: ====', i)
                print('卖家数量:=====', len(prices))
                # print('原始值：====', d[i])
                try:
                    idx = name_list.index('ctss1897')
                    want_price = price_list[idx].split( )[0]

                    print('the new price is ****** ctss1897 ******: =====', want_price)
                    b[i] = want_price
                    d[i] = 'ctss1897'
                    modifiy_list.append(int(i)+1)
                    print("==================end=======================")
                    continue

                except Exception as e:
                    print('没有ctss1897 !!!!!')

                try:
                    idx = name_list.index('seventeeeeeeen')
                    want_price = price_list[idx]
                    print('the new price is ****** seventeeeeeeen ******: =====', want_price)
                    b[i] = want_price
                    d[i] = 'seventeeeeeeen'
                    modifiy_list.append(int(i)+1)
                    print("==================end=======================")
                    continue
                except Exception as e:
                    raise e

                print('没有找到要找的用户名！！！！！！！！')


        print('价格：')
        for i in b:
            print(i)
        print('seller:')
        for i in d:
            print(i)
        print('修改的列')
        for i in modifiy_list:
            print(i)


        with open('newprice.txt', 'w') as f:
            for item in b:
                f.write(str(item) + '\n')
        f.close()

        with open('newseller.txt', 'w') as f:
            for item in d:
                f.write(item + '\n')
        f.close()

        with open('changedline.txt', 'w') as f:
            for item in modifiy_list:
                f.write(str(item) + '\n')
        f.close()

        # for item in a:
        #     browser.get("https://uae.souq.com/ae-en/")
        #     browser.find_element_by_css_selector(".input-group input").send_keys(Keys.CONTROL, "a")
        #     browser.find_element_by_css_selector(".input-group input").send_keys(item)
        #     browser.find_element_by_css_selector(".input-group-button button").click()
        #     # 等待加载完成
        #     time.sleep(2)
        #     try:
        #         span = browser.find_element_by_css_selector(".price.is.sk-clr1").get_attribute('textContent')
        #         b = browser.find_element_by_css_selector(".unit-seller-link b").get_attribute('textContent')
        #         price = span.split( )[0]
        #         print('ean: ', item)
        #         print('价格：==================================================================',price)
        #         seller = b
        #         print('seller is ==================================', seller)
        #         url = browser.current_url
        #         print('url为 ==============================================',url)

        #         price_list.append(price)
        #         url_list.append(url)
        #         seller_list.append(seller)
        #     except:
        #         print('========================================没找到===============================')
        #         price_list.append(0)
        #         url_list.append('not found')
        #         seller_list.append('dont know')
        #     # break

        # print('ean:', len(a))
        # print('循环结束')
        # for i in url_list:
        #     print(i)
        # print('价格：')
        # for i in price_list:
        #     print(i)
        # print('seller:')
        # for i in seller_list:
        #     print(i)

        # with open('url.txt', 'w') as f:
        #     for item in url_list:
        #         f.write(item + '\n')
        # f.close()

        # with open('price.txt', 'w') as f:
        #     for item in price_list:
        #         f.write(item + '\n')
        # f.close()

        # with open('seller.txt', 'w') as f:
        #     for item in seller_list:
        #         f.write(item + '\n')
        # f.close()



    def parse(self, response):
        pass
