#encoding:utf-8
import scrapy
import re
#from bs4 import BeautifulSoup
import urllib2
from scrapy.http import Request
from ..items import MytestItem
import json

class mytestfirst(scrapy.Spider):
     name="mytestfirst"
     handle_httpstatus_list=[404,500]
     allowed_domains=['taobao.com']
     start_urls=[
            "http://www.taobao.com/",
     ]

     def parse(self,response):
         key="女包";
         for i in range(0,1):
             url="https://s.taobao.com/search?search_type=item&q="+str(key)+"&s="+str(i*44)
             request=Request(url=url,callback=self.page)
             if response.status in self.handle_httpstatus_list:
                 print("main page is wrong!")
                 continue
             else:
                 yield  request
                 #request.meta['parseUrl']=url;


     def page(self,response):

         if response.status in self.handle_httpstatus_list:
            print("maincoming page is wrong!")
            pass
         else:
             body=response.body.decode('utf-8','ignore')
             #reg=u"[\u4e00-\u9fa5]"
             #ip=".*?"
             #soup=BeautifulSoup(body,"html.parser")
             #title=soup.find('a',attrs={'href':'//www.tmall.com'})
             #title=response.xpath("//title/text()").extract()
             #title=response.xpath('//*[@id="srp-footer"]/ div/div[1]/p/span[3]/a').extract()
             re_words = re.compile('g_page_config = {(.*?):false}}').findall(body)
             _re_words="{"+re_words[0]+":false}}"
             _format=_re_words.replace('\r','').replace('\n','').replace('\t','')
             s=json.loads(_format);
             #pageItem=MytestItem();
             #print s['mods']['itemlist']['data']['auctions'][0]['view_sales']
             for index,val in enumerate(s['mods']['itemlist']['data']['auctions']):

                 pageItem=MytestItem()
                 pageItem['singleUrl']=val['detail_url']
                 pageItem['singleTitle']=val['raw_title']
                 pageItem['singleArea']=val['item_loc']
                 pageItem['singleDes']=val['title']
                 pageItem['singleId']=val['nid']
                 sellerId=val['user_id']#卖家ID
                 rate_url_good="https://rate.tmall.com/list_detail_rate.htm?itemId="+str(val['nid'])+"&sellerId="+sellerId+"&order=3&currentPage=1&append=0&content=1"
                 rate_url="https://dsr-rate.tmall.com/list_dsr_info.htm?itemId="+str(val['nid'])
                 #print(rate_url_good)
                 # rateTotal=self.singleRate(rate_url)
                 #yield scrapy.Request(url=rate_url,meta={'item':pageItem},callback=self.singleRate,dont_filter=True)
                 return scrapy.Request(url=rate_url_good,meta={'item':pageItem},callback=self.singleRateGood,dont_filter=True)
                 # pageItem['singleRareTotalRe']=rateTotal['rareTotalRe']
                 # pageItem['singleGradeAvge']=rateTotal['gradeAvg']
                 # rateGood=self.singleRateGood(rate_url_good)
                 # pageItem['singlePicNum']=rateGood['picNum']
                 # pageItem['singleUsed']=rateGood['used']
                 # #print pageItem
                 #yield pageItem

     def singleRate(self,response):
          #def singleRate(self,url,repeatQequestTimes=5):
         """
         查找商品指数和好评总数量
         :param url:gradeAvg：商品指数 rateEval:评论总数
         :return:
         """
         if response.status in self.handle_httpstatus_list:
            print("singleRate page is wrong!")
            pass
         else:
             pageItem = response.meta['item']
             body=response.body.decode('utf-8','ignore')
             rateTotalRe=re.compile('"dsr":(.*?)\}\)').findall(body)
             rateEval=eval(rateTotalRe[0])
             pageItem['singleRareTotalRe']=rateEval['rateTotal']
             pageItem['singleGradeAvge']=rateEval['gradeAvg']
             print(response.url)
             print(pageItem['singleRareTotalRe']+'-----'+pageItem['singleGradeAvge'])
            # return pageItem
         #copyUrl=url
         #response=urllib2.urlopen(str(url))
         # try:
         #     body=response.read();
         #     rateTotalRe=re.compile('"dsr":(.*?)\}\)').findall(body)
         #     rateEval=eval(rateTotalRe[0])
         #     return {'rareTotalRe':rateEval['rateTotal'],'gradeAvg':rateEval['gradeAvg']}
         # except urllib2.URLError as e:
         #     if(repeatQequestTimes>0):
         #         if hasattr(e,'code') and 300 <=e.code<600:
         #             print("singeRate download error:"+e.reason)
         #             return self.singleRate(self,url,repeatQequestTimes-1)


     def singleRateGood(self,response):

         """
         获取有图的评论总数和追评总数
         :param url:used:追评数 picNum:有图评论
         :return:
         """
         if response.status in self.handle_httpstatus_list:
            print("singleRateGood page is wrong!")
            pass
         else:
             pageItem = response.meta['item']
             body=response.body.decode('utf-8','ignore')
             rateTotalRe=re.compile('"rateCount":(.*?),"rateDanceInfo"').findall(body)
             rateEval=eval(rateTotalRe[0])
             pageItem['singlePicNum']=rateEval['picNum']
             pageItem['singleUsed']=rateEval['used']
             #print(pageItem)
             return pageItem
         #copyUrl=url
         # response=urllib2.urlopen(str(url))
         # try:
         #     body=response.read();
         #     rateTotalRe=re.compile('"rateCount":(.*?),"rateDanceInfo"').findall(body)
         #     rateEval=eval(rateTotalRe[0])
         #     return {'picNum':rateEval['picNum'],'used':rateEval['used']}
         # except urllib2.URLError as e:
         #     if(repeatQequestTimes>0):
         #         if hasattr(e,'code') and 300 <=e.code<600:
         #             print("singleRateGood download error:"+e.reason)
         #             return self.singleRateGood(self,url,repeatQequestTimes-1)






















