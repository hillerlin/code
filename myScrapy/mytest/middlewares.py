# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from random import choice
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .agents import AGENTS
from .db import RedisClient
import urllib


class MytestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class JavaScriptMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        s.conn = RedisClient()
        return s

    def process_request(self, request, spider):
        agent = choice(AGENTS)
        request.headers['User-Agent'] = agent
        if agent:
            # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
            order = "d168f83eca5a334b2e30fa051bf424f0";
            # 获取IP的API接口
            apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + str(order)+'&sep=3';
            # 获取IP列表
            res = urllib.urlopen(apiUrl).read().strip("\n");
            # 按照\n分割获取到的IP
            ips = res.split("\n");
            print('proxy is working ip:'+str(ips[0]))
            # driver = webdriver.PhantomJS(executable_path="D:\Python27\Tools\phantomjs-2.1.1-windows/bin\phantomjs.exe",service_args=['--load-images=false','--disk-cache=true','--proxy={}'.format(ips[0]), '--proxy-type=socks5']) #指定使用的浏览器
            # #wait = WebDriverWait(driver, 10)
            # # driver = webdriver.Firefox()
            # driver.get(request.url)
            # time.sleep(70)
            # #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#j-product-desc > div.ui-box.product-property-main > div.ui-box-title')))
            # js = "var q=document.documentElement.scrollTop=10000"
            # driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
            # body = driver.page_source
            # print(body)
            chromeOptions = webdriver.ChromeOptions()# 设置代理
            chromeOptions.add_argument("--proxy-server =http://{}".format(ips[0]))
            webdriver.Proxy()
            browser = webdriver.Chrome(executable_path='D:\Python27\Tools\chromedriver_win32/chromedriver.exe',chrome_options = chromeOptions)
            #wait = WebDriverWait(browser, 10)
            browser.get(request.url)
            body = browser.page_source
            print(body)
            browser.set_window_size(1400, 900)
            return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
    # def process_response(self,request, response, spider):
    #     if response.status == 200:
    #         print "PhantomJS is starting..."
    #         driver = webdriver.PhantomJS(executable_path="D:\Python27\Tools\phantomjs-2.1.1-windows/bin\phantomjs.exe",service_args=['--load-images=false','--disk-cache=true','--proxy=127.0.0.1:10800', '--proxy-type=socks5']) #指定使用的浏览器
    #         wait = WebDriverWait(driver, 5)
    #         # driver = webdriver.Firefox()
    #         driver.get(request.url)
    #         time.sleep(3)
    #         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#j-product-description > div.ui-box-title')))
    #         js = "var q=document.documentElement.scrollTop=10000"
    #         driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
    #         body = driver.page_source
    #         return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
