# coding=utf-8
import scrapy
import re
#from bs4 import BeautifulSoup
import urllib2
from scrapy.http import Request
from scrapy import Selector
from ..items import Yindouwang
#import json
import sys
import chardet
#import io
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class yindouwang(scrapy.Spider):
     name="yindouwang"
     handle_httpstatus_list=[404,500]
     _page=2
     allowed_domains=['yindou.com']
     start_urls=[
            "https://www.yindou.com/zhaiquangoumai/?page=2&total=2802&rate=0&guarantee_id_code=&leftday=0&backday=0",

     ]

     def parse(self,response):
         totalPage=176
         pathList={'body':'/html/body/div[2]/article/div/div/div[1]/div[2]/div[2]/div'}
         bodyList=response.selector.xpath(pathList['body']).extract()
         if(bodyList and self._page<4):
             self._page+=1
             for index,value in enumerate(bodyList):
                 url=Selector(text=value).xpath('//span[7]/a/@href').extract()[0]
                 yield scrapy.Request(url=url,cookies={'PHPSESSID':'0pnglqi9n9q6ototh6skpslb67',
                                           '__jsluid':'a8a08442bcb30fa94fcc184d0edd1619',
                                           'gr_user_id':'dd9cb2dd-f8d8-430c-9ebd-d93f310f9450',
                                           'ydrecord':'533220_1495088148',
                                           'gr_session_id_b9a32bc6f5df5804':'ab02d7a9-5771-4db0-abcd-335892026d61'},
                         callback=self.page)

             _url='https://www.yindou.com/zhaiquangoumai/?page='+str(self._page)+'&total=2802&rate=0&guarantee_id_code=&leftday=0&backday=0'
             bodyList=scrapy.Request(url=_url,cookies={'PHPSESSID':'0pnglqi9n9q6ototh6skpslb67',
                                           '__jsluid':'a8a08442bcb30fa94fcc184d0edd1619',
                                           'gr_user_id':'dd9cb2dd-f8d8-430c-9ebd-d93f310f9450',
                                           'ydrecord':'533220_1495088148',
                                           'gr_session_id_b9a32bc6f5df5804':'ab02d7a9-5771-4db0-abcd-335892026d61'},
                         callback=self.parse)
             yield bodyList

     def subPage(self,response):
         pathList={'body':'/html/body/div[2]/article/div/div/div[1]/div[2]/div[2]/div'}
         bodyList=response.selector.xpath(pathList['body']).extract()
         for index,value in enumerate(bodyList):
              url=Selector(text=value).xpath('//span[7]/a/@href').extract()[0]
              print(url)
              request=Request(url=url,cookies={'PHPSESSID':'0pnglqi9n9q6ototh6skpslb67',
                                           '__jsluid':'a8a08442bcb30fa94fcc184d0edd1619',
                                           'gr_user_id':'dd9cb2dd-f8d8-430c-9ebd-d93f310f9450',
                                           'ydrecord':'533220_1495088148',
                                           'gr_session_id_b9a32bc6f5df5804':'ab02d7a9-5771-4db0-abcd-335892026d61'},
                         callback=self.page)
         yield request;



     def page(self,response):
         if response.status in self.handle_httpstatus_list:
            print("maincoming page is wrong!")
            pass
         else:
             pathList={'bidlist':'/html/body/div[2]/article/div/div[2]/div[2]/div[5]/div[1]/div/div[2]/div',
                       'pro_rate':'/html/body/div[2]/article/div/div[2]/div[1]/div[1]/div[1]/div[1]/p[1]/span/text()',
                       'pro_limit':'/html/body/div[2]/article/div/div[2]/div[1]/div[1]/div[1]/div[2]/p[1]/span/text()',
                       'pro_price':'/html/body/div[2]/article/div/div[2]/div[1]/div[1]/div[1]/div[3]/p[1]/span/text()',
                       'pro_end_time':'/html/body/div[2]/article/div/div[2]/div[2]/div[5]/div[2]/div/div[2]/div[1]/span[1]/text()',
                       'repaymentTime':'/html/body/div[2]/article/div/div[2]/div[1]/div[1]/div[1]/div[4]/p[1]/span/text()',
                       'pro_name':'/html/body/div[2]/article/div/div[2]/div[1]/div[1]/p[1]/a'}
             item=Yindouwang()
             item['pro_rate']=pro_rate=response.selector.xpath(pathList['pro_rate']).extract()[0]
             item['pro_price']= pro_price=response.selector.xpath(pathList['pro_price']).extract()[0]
             item['pro_limit']=pro_limit=response.selector.xpath(pathList['pro_limit']).extract()[0]
             item['pro_end_time']= pro_end_time=self.timeTostring(response.selector.xpath(pathList['pro_end_time']).extract()[0])
             item['pro_start_time']= pro_start_time=self.timeTostring(response.selector.xpath(pathList['repaymentTime']).extract()[0])-86400*int(pro_limit)
             item['pro_name']=pro_name=response.selector.xpath(pathList['pro_name']+'/text()').extract()[0]
             item['pro_id']=pro_id=response.selector.xpath(pathList['pro_name']+'/@href').re('(\d+)\.html')[0]
             item['pro_type_dsc']='个人借贷'
             recordList=[]
             buyRecordList=response.selector.xpath(pathList['bidlist']).extract()
             for index,value in enumerate(buyRecordList):
                   user_name=Selector(text=value).xpath('//div/span[1]/text()').extract()[0]
                   _user_bid_price=Selector(text=value).xpath('//div/span[2]/text()').re('(\d+\.\d+)|(\d+)')
                   user_bid_price=_user_bid_price[0] if _user_bid_price[0] else _user_bid_price[1]
                   user_buy_time=Selector(text=value).xpath('//div/span[3]/text()').extract()[0]
                   recordList.append({'user_bid_price':user_bid_price,'user_name':user_name,'user_buy_time':self.timeTostring(user_buy_time,2),'pro_id':item['pro_id']})
                   # recordList['user_bid_price']=user_bid_price
                   # recordList['user_name']=user_name
                   #item['user_record_list'][index]['user_name']=user_name
                   #item['user_record_list'][index]['user_bid_price']=user_bid_price
                   #print(recordList)
             item['user_record_list']=recordList
             yield item
             # f = open("text.txt",'wb')
             # f.write(body)
             # f.close()

     def timeTostring(self,_time,type=1):
         """
         :type=1 是格式化年月日的类型，:type=2 是格式化带有时分秒的类型
         """
         if(type==1):
             timeArray = time.strptime(_time, "%Y-%m-%d")
         else:
             timeArray = time.strptime(_time,"%Y-%m-%d %H:%M:%S")

         timeStamp = int(time.mktime(timeArray))
         return timeStamp
     # def singleRate(self,response):
     #      #def singleRate(self,url,repeatQequestTimes=5):
     #     """
     #     查找商品指数和好评总数量
     #     :param url:gradeAvg：商品指数 rateEval:评论总数
     #     :return:
     #     """
     #     if response.status in self.handle_httpstatus_list:
     #        print("singleRate page is wrong!")
     #        pass
     #     else:
     #         pageItem = response.meta['item']
     #         body=response.body.decode('utf-8','ignore')
     #         rateTotalRe=re.compile('"dsr":(.*?)\}\)').findall(body)
     #         rateEval=eval(rateTotalRe[0])
     #         pageItem['singleRareTotalRe']=rateEval['rateTotal']
     #         pageItem['singleGradeAvge']=rateEval['gradeAvg']
     #         print(response.url)
     #         print(pageItem['singleRareTotalRe']+'-----'+pageItem['singleGradeAvge'])



     # def singleRateGood(self,response):
     #
     #     """
     #     获取有图的评论总数和追评总数
     #     :param url:used:追评数 picNum:有图评论
     #     :return:
     #     """
     #     if response.status in self.handle_httpstatus_list:
     #        print("singleRateGood page is wrong!")
     #        pass
     #     else:
     #         pageItem = response.meta['item']
     #         body=response.body.decode('utf-8','ignore')
     #         rateTotalRe=re.compile('"rateCount":(.*?),"rateDanceInfo"').findall(body)
     #         rateEval=eval(rateTotalRe[0])
     #         pageItem['singlePicNum']=rateEval['picNum']
     #         pageItem['singleUsed']=rateEval['used']
     #         return pageItem























