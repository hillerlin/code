# -*- coding: utf-8 -*-
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.common.proxy import Proxy, ProxyType
from config import *
import pymongo
import urllib
import time

# client = pymongo.MongoClient(MONGO_URL)
# db = client[MONGO_DB]

#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
#chromeOptions = webdriver.ChromeOptions()# 设置代理
#fireboxOptions=webdriver.FirefoxOptions()
# order = "d168f83eca5a334b2e30fa051bf424f0";
# # 获取IP的API接口
# apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + str(order)+'&sep=3';
# # 获取IP列表
# res = urllib.urlopen(apiUrl).read().strip("\n");
# # 按照\n分割获取到的IP
# ips = res.split("\n");
# print('proxy ip is:',ips[0])
# #chromeOptions.add_argument(["--proxy-server = http://{}".format(ips[0])])
# #fireboxOptions.add_argument(["--proxy-server = http://{}".format(ips[0])])
# webdriver.Proxy()
# #browser = webdriver.Chrome(executable_path='D:\Python27\Tools\chromedriver_win32/chromedriver.exe',chrome_options = chromeOptions)
# browser = webdriver.Firefox(executable_path='D:\Python27\Tools\geckodriver\geckodriver.exe')
# wait = WebDriverWait(browser, 10)
# browser.set_window_size(1400, 900)

def search():
    print('正在搜索')
    try:
        order = "d168f83eca5a334b2e30fa051bf424f0";
        # 获取IP的API接口
        apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + str(order)+'&sep=3';
        # 获取IP列表
        res = urllib.urlopen(apiUrl).read().strip("\n");
        # 按照\n分割获取到的IP
        ips = res.split("\n");
        print('proxy ip is:',ips[0])
        proxyIp = ips[0];
        id=re.compile(r'(.*?):(.*)').findall(proxyIp)[0]
        _ip=id[0]
        port=id[1]
        # 使用代理
        #chromeOptions.add_argument(["--proxy-server = http://{}".format(ips[0])])
        #fireboxOptions.add_argument(["--proxy-server = http://{}".format(ips[0])])
        #browser = webdriver.Chrome(executable_path='D:\Python27\Tools\chromedriver_win32/chromedriver.exe',chrome_options = chromeOptions)
        myProxy = ips[0]

        # proxy = Proxy({
        #     'proxyType': ProxyType.MANUAL,
        #     'httpProxy': myProxy,
        #     'ftpProxy': myProxy,
        #     'sslProxy': myProxy,
        #     'noProxy': '' # set this value as desired
        #     })
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", _ip)
        profile.set_preference("network.proxy.http_port", int(port))
        profile.update_preferences()
        browser = webdriver.Firefox(executable_path='D:\Python27\Tools\geckodriver\geckodriver.exe',firefox_profile=profile)
        wait = WebDriverWait(browser, 10)
        browser.set_window_size(1400, 900)
        browser.set_page_load_timeout(10)
        browser.get('https://www.aliexpress.com/store/product/SHEIN-Color-Block-Womens-Tops-and-Blouses-Multicolor-Long-Sleeve-V-Neck-Belted-Blouse-Bishop-Sleeve/1159363_32850275270.html?spm=2114.12010615.0.0.b3e6c23kyngXj')
        #browser.get('https://www.aliexpress.com/item/Hugcitar-2017-autumn-Hoodies-Sweatshirt-Women-Long-Sleeve-Women-s-Clothing-letters-print-pink-white-solid/1000004539419.html?spm=2114.search0103.3.9.66cfea01VS191D&ws_ab_test=searchweb0_0,searchweb201602_3_10152_10151_10065_10068_10344_10342_10325_10546_10343_10340_10548_10341_10084_10617_10083_10616_10615_10307_10313_10059_10534_100031_10604_10103_10142,searchweb201603_32,ppcSwitch_4&algo_expid=b5bee4d6-265b-4748-8429-32517af41728-1&algo_pvid=b5bee4d6-265b-4748-8429-32517af41728&priceBeautifyAB=1')

        #browser.get('http://www.ip.cn/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#j-product-desc > div.ui-box.product-property-main > div.ui-box-title'))
        )
        contents=browser.page_source
        print('---------------------')
        browser.close()
        print(contents)
        # submit = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        # input.send_keys(KEYWORD)
        # submit.click()
        # total = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        # get_products()
        # return total.text
    except TimeoutException:
        #browser.close()
        contents=browser.page_source
        print(contents)
        return search()


def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        # if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)


def main():
  search()

if __name__ == '__main__':
    main()
