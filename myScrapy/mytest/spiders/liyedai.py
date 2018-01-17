# coding=utf-8
import scrapy
import re
#from bs4 import BeautifulSoup
import urllib2
from scrapy.http import Request
from scrapy import Selector
from ..items import liyedaiProduct
#import json
import sys
import chardet
#import io
import time
#from dateutil.relativedelta import relativedelta
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

class liyedai(scrapy.Spider):
     name="liyedai"
     handle_httpstatus_list=[404,500]
     _page=2
     proUrlPrefix='http://www.liyedai.cn/front/invest/invest?bidId='
     allowed_domains=['liyedai.cn']
     start_urls=[
            "http://www.liyedai.cn/front/invest/investHome?currPage=2&type=&bidType=&apr=&period=&amount=&loanSchedule=&keywords=",

     ]

     def parse(self,response):
         pathList={'body':'/html/body/div[3]/div/div[2]/table/tbody/tr'}
         bodyList=response.selector.xpath(pathList['body']).extract()
         for index,value in enumerate(bodyList):
             if(index<1):
                 stringId=re.compile('\d+').findall(Selector(text=value).xpath("//td[1]/a/@href").extract()[0])[0]#查出汇总页面上的所有标的ID
                 proUrl='http://www.liyedai.cn/front/invest/invest?bidId='+stringId
                 #print(proUrl)
                 yield Request(url=proUrl,cookies={'PLAY_SESSION':'"30f7d526f4bba14857d95006a2f395ae98264dc4-___ID=c83bb35f-7c82-455b-b595-04b9da123442&userId=5474601543"',
                                                       'UM_distinctid':'15c15d7134f43f-08c21b85c0a5c-414a0229-1fa400-15c15d71351528',
                                                       'Hm_lvt_d9d55fd4628e13c04a919c89181a2976':'1495015036',
                                                       'Hm_lpvt_d9d55fd4628e13c04a919c89181a2976':'1495177061',
                                                       'CNZZDATA1256299900':'1795223197-1495014591-%7C1495177364',
                                                       'PLAY_ERRORS':'',
                                                       'PLAY_FLASH':'',
                                                       'userId':'5474601543'},callback=self.page)
             #print(stringId)
             # proUrl='http://www.liyedai.cn/front/invest/invest?bidId=11940'
             # yield scrapy.Request(url=proUrl,cookies={'PLAY_SESSION':'"30f7d526f4bba14857d95006a2f395ae98264dc4-___ID=c83bb35f-7c82-455b-b595-04b9da123442&userId=5474601543"',
             #                                           'UM_distinctid':'15c15d7134f43f-08c21b85c0a5c-414a0229-1fa400-15c15d71351528',
             #                                           'Hm_lvt_d9d55fd4628e13c04a919c89181a2976':'1495015036',
             #                                           'Hm_lpvt_d9d55fd4628e13c04a919c89181a2976':'1495177061',
             #                                           'CNZZDATA1256299900':'1795223197-1495014591-%7C1495177364',
             #                                           'PLAY_ERRORS':'',
             #                                           'PLAY_FLASH':'',
             #                                           'userId':'5474601543'},callback=self.page)
         # pathList={'body':'/html/body/div[3]/div/div[2]/table/tbody/tr'}
         # bodyList=response.selector.xpath(pathList['body']).extract()
         # for index,value in enumerate(bodyList):
         #     proUrl=self.proUrlPrefix+str(Selector(text=value).xpath('//tr/td[7]/a/@href').re('\=(\d+)')[0])
         #     yield scrapy.Request(url=proUrl,cookies={'PLAY_SESSION':'30f7d526f4bba14857d95006a2f395ae98264dc4-___ID=c83bb35f-7c82-455b-b595-04b9da123442&userId=5474601543',
         #                                   'UM_distinctid':'15c15d7134f43f-08c21b85c0a5c-414a0229-1fa400-15c15d71351528'},
         #                 callback=self.page)

         #print(bodyList)
         # totalPage=176
         # pathList={'body':'/html/body/div[2]/article/div/div/div[1]/div[2]/div[2]/div'}
         # bodyList=response.selector.xpath(pathList['body']).extract()
         # if(bodyList and self._page<4):
         #     self._page+=1
         #     pathList={'body':'/html/body/div[2]/article/div/div/div[1]/div[2]/div[2]/div'}
         #     bodyList=response.selector.xpath(pathList['body']).extract()
         #     for index,value in enumerate(bodyList):
         #         url=Selector(text=value).xpath('//span[7]/a/@href').extract()[0]
         #         #print(url)
         #         yield scrapy.Request(url=url,cookies={'PHPSESSID':'0pnglqi9n9q6ototh6skpslb67',
         #                                   '__jsluid':'a8a08442bcb30fa94fcc184d0edd1619',
         #                                   'gr_user_id':'dd9cb2dd-f8d8-430c-9ebd-d93f310f9450',
         #                                   'ydrecord':'533220_1495088148',
         #                                   'gr_session_id_b9a32bc6f5df5804':'ab02d7a9-5771-4db0-abcd-335892026d61'},
         #                 callback=self.page)
         #
         #     _url='https://www.yindou.com/zhaiquangoumai/?page='+str(self._page)+'&total=2802&rate=0&guarantee_id_code=&leftday=0&backday=0'
         #        #url='https://www.yindou.com/zhaiquangoumai/?page=2&total=2802&rate=0&guarantee_id_code=&leftday=0&backday=0'
         #     bodyList=scrapy.Request(url=_url,cookies={'PHPSESSID':'0pnglqi9n9q6ototh6skpslb67',
         #                                   '__jsluid':'a8a08442bcb30fa94fcc184d0edd1619',
         #                                   'gr_user_id':'dd9cb2dd-f8d8-430c-9ebd-d93f310f9450',
         #                                   'ydrecord':'533220_1495088148',
         #                                   'gr_session_id_b9a32bc6f5df5804':'ab02d7a9-5771-4db0-abcd-335892026d61'},
         #                 callback=self.parse)
         #     yield bodyList

     def page(self,response):
         if response.status in self.handle_httpstatus_list:
            print("maincoming page is wrong!")
            pass
         else:
             pathList={'bidlist':'/html/body/div[3]/div/div[1]/div[2]/div/ul[1]/li',
                       'pro_rate':'/html/body/div[3]/div/div[1]/div[2]/div/ul[1]/li[2]/div/span/text()',
                       'pro_limit':'/html/body/div[3]/div/div[1]/div[2]/div/ul[1]/li[3]/div/span/text()',
                       'pro_price':'/html/body/div[3]/div/div[1]/div[2]/div/ul[1]/li[1]/div/span',
                       'pro_end_time':'/html/body/div[2]/article/div/div[2]/div[2]/div[5]/div[2]/div/div[2]/div[1]/span[1]/text()',
                       'pro_start_time':'/html/body/div[3]/div/div[1]/div[2]/div/ul[2]/li[5]/span/text()',
                       'pro_name':'/html/body/div[3]/div/div[1]/div[2]/div/div[2]/h4/text()',
                       'pro_id':'//*[@id="bidImgGallery"]',
                       'sign':'//*[@id="bidInvestRecords"]/@data-bid-sign'}
             item=liyedaiProduct()
             pro_rate=response.selector.xpath(pathList['pro_rate']).re('(\d+\.\d+)')
             item['pro_rate']=float(pro_rate[0])+float(pro_rate[1]) if pro_rate[1] else pro_rate[0]
             item['pro_price']= pro_price=response.selector.xpath(pathList['pro_price']).re('(\d+\.\d+)')[0]
             item['pro_limit']=pro_limit=response.selector.xpath(pathList['pro_limit']).re('\d+')[0]#24个月
             item['pro_start_time']= pro_start_time=self.timeTostring(response.selector.xpath(pathList['pro_start_time']).re('\d+\-\d+\-\d+')[0])
             item['pro_end_time']= pro_end_time=self.timeTostring(unicode(datetime.date.fromtimestamp(float(pro_start_time))+relativedelta(months=+int(pro_limit))))
             item['pro_name']=pro_name=response.selector.xpath(pathList['pro_name']).extract()[0]
             item['pro_id']=pro_id=re.compile('(\d+)').findall(response.url)[0]
             item['pro_type_dsc']='个人借贷'
             sign=response.selector.xpath(pathList['sign']).extract()[0]#每个标的的投资签名
             temperUrl="http://www.liyedai.cn/front/invest/viewBidInvestRecords?pageNum=1&pageSize=10&bidIdSign="+sign;
             item['user_record_list']=self.feeder(temperUrl,pro_id)
             yield item;

     def feeder(self,url,proId=0,repeatQequestTimes=3):
         response=urllib2.urlopen(str(url))
         try:
             recordList=[]
             body=response.read();
             _xath="/html/body/table/tbody/tr"
             text=Selector(text=body).xpath(_xath).extract()
             for index,value in enumerate(text):
                 user_name=Selector(text=value).xpath('//td[1]/text()').extract()[0]

                 user_bid_price=Selector(text=value).xpath('//td[2]/text()').re('\d+\.\d+')[0]

                 user_buy_time=Selector(text=value).xpath('//td[4]/text()').extract()[0]

                 recordList.append({'user_bid_price':user_bid_price,'user_name':user_name,'user_buy_time':self.timeTostring(user_buy_time,2),'pro_id':proId})
             return recordList

              #return recordList


         except urllib2.URLError as e:
             if(repeatQequestTimes>0):
                 if hasattr(e,'code') and 300 <=e.code<600:
                     print("singeRate download error:"+e.reason)
                     return self.feeder(self,url,proId,repeatQequestTimes-1)


     def singleRate(self,response):
         """
         查找商品指数和好评总数量
         :param url:gradeAvg：商品指数 rateEval:评论总数
         :return:
         """
         if response.status in self.handle_httpstatus_list:
            print("singleRate page is wrong!")
            pass
         else:
             #item =response.meta['item']
             print('50')
             #return item

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























