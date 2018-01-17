#encoding:utf-8
import re
import urllib2
from itertools import *
import sys
import chardet
#import io
# reload(sys)
# sys.setdefaultencoding('utf-8')
#import json
# def download(url,user_agent='wswp',requestTimes=2):
#     print 'Downloading:',url
#     #设置简单的代理
#     headers={'User-agent':user_agent}
#     request=urllib2.Request(url,headers=headers)
#     try:
#         html=urllib2.urlopen(request).read()
#     except urllib2.URLError as e:
#         print 'Download error:',e.errno
#         html=0
#         if(requestTimes>0):
#             #当服务端代码500的时候重新请求两次
#             if hasattr(e,'code') and 500<=e.code<600 :
#                 return download(url,requestTimes-1)
#
#     return html.decode('utf-8').encode('gb18030')
#
# print(download('https://uc.jcloud.com/login?returnUrl=http://uc.jcloud.com/activity/queryActivity.action%3Fuuid%3Df3cbe4a9-6df9-4fa1-a3e3-9fe839be8d4f'))
#rlt = imap(pow, [1, 2, 3], [1, 2, 3])
# rlt = ifilterfalse(lambda x: x > 5, [2, 3, 5, 6, 7])
#
# for num in rlt:
#     print(num)
# for m, n in product('abc', [1, 2]):
#     print m, n

# def height_class(h):
#     if h > 180:
#         return "tall"
#     elif h < 160:
#         return "short"
#     else:
#         return "middle"
#
# friends = [191, 158, 159, 165, 170, 177, 181, 182, 190]
#
# friends = sorted(friends, key = height_class)
# print(friends)
# for m, n in groupby(friends, key = height_class):
#     print(m)
#     print(list(n))

# L = [{1:5,3:4},{1:3,6:3},{1:1,2:4,5:6},{1:9}]
# def f2(a,b):
#     return a[1]-b[1]
# L.sort(cmp=f2)
# print L
# a=[1,2,3,4,5]
# b=set(a)
# print(b)
#JsonStr = json.dumps( aa, ensure_ascii=False, encoding='UTF-8')
#print(JsonStr)
# class washer:
#     def __init__(self,water=100,sour=2):
#         self._water=water
#         self.sour=sour
#
# if __name__ == '__main__':
#     ws=washer()
#     aa=ws.water
#     bb=1
# def f(x,l=[]):
#     for i in range(x):
#         l.append(i*i)
#     print l
# a=['1','b','c']
# b='_'.join(a)
# print(b)
#("#btn-bid-record-more").text("鐐瑰嚮灞曞紑鏇村鎶曡祫璁板綍")'
# import cookielib
# class WhySpider:
#
#     # 初始化爬虫
#     def __init__(self):
#         self.cookie_jar = cookielib.CookieJar()
#         self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
#         self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'}
#
#     # 发送GET请求
#     def send_get(self,get_url):
#         result = ""
#         try:
#             my_request = urllib2.Request(url = get_url, headers = self.headers)
#             result = self.opener.open(my_request).read()
#         except Exception,e:
#             print "Exception : ",e
#        # return chardet.detect(result)
#         return result
#
#     # 发送POST请求
#     def send_post(self,post_url,post_data):
#         result = ""
#         try:
#             my_request = urllib2.Request(url = post_url,data = post_data, headers = self.headers)
#             result = self.opener.open(my_request).read()
#         except Exception,e:
#             print "Exception : ",e
#         f = open("text.txt",'wb')
#         f.write(result)
#         f.close()
#         return result
#
#     # 模拟电脑
#     def set_computer(self):
#         user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
#         self.headers = { 'User-Agent' : user_agent }
#
#     # 模拟手机
#     def set_mobile(self):
#         user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25'
#         self.headers = { 'User-Agent' : user_agent }
#
# my_spider = WhySpider()
#
# # 模拟GET操作
# #print my_spider.send_get('http://3.apitool.sinaapp.com/?why=GetString2333')
#
# # 模拟POST操作
# print my_spider.send_post('https://www.yindou.com/zhaiquangoumai/3842.html','why=PostString2333')
# import time
# a='2013-10-10'
# timeArray = time.strptime(a, "%Y-%m-%d")
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)
from dateutil.relativedelta import relativedelta
import datetime
import time
print(datetime.date.fromtimestamp(float('1496146396.31'))+ relativedelta(months=+1))

