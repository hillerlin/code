# coding=utf-8
import scrapy
import re
#from bs4 import BeautifulSoup
import urllib2
from scrapy.http import Request
from scrapy import Selector
from ..items import smtconfig
import json
import sys
import time
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

class smt(scrapy.Spider):
     name="smt"
     handle_httpstatus_list=[404,500]
     _page=1
     #allowed_domains=['aliexpress.com']
     start_urls=[
            #"https://www.aliexpress.com/store/3026024/search/2.html?spm=2114.12010615.0.0.e119e1afYcSu2&origin=n&SortType=bestmatch_sort",
            #"https://www.aliexpress.com/store/all-wholesale-products/1752153.html?spm=2114.12010608.0.0.5597e5c58EqJzh",
            #"https://www.aliexpress.com/store/1752153/search/2.html?spm=2114.12010615.0.0.690106dcnzkT0h&origin=n&SortType=bestmatch_sort",
            #"https://www.aliexpress.com/store/1495459/search/1.html?spm=2114.12010615.0.0.49fee69faWBLxR&origin=n&SortType=bestmatch_sort",
            "https://shein.aliexpress.com/store/1159363/search/2.html?spm=2114.12010615.0.0.56721044xPMPBJ&origin=n&SortType=bestmatch_sort",

     ]

     def start_requests(self):
          yield scrapy.Request(url="https://www.aliexpress.com/store/product/SHEIN-Color-Block-Womens-Tops-and-Blouses-Multicolor-Long-Sleeve-V-Neck-Belted-Blouse-Bishop-Sleeve/1159363_32850275270.html?spm=2114.12010615.0.0.b3e6c23kyngXj",
                               callback=self.page)


     def parse(self,response):
         pathList={'body':'//*[@id="list-items"]/ul/li','body_2':'//*[@id="node-gallery"]/div[5]/div/div/ul/li'}
         #body=response.body.decode('utf-8','ignore')
         bodyList=response.selector.xpath(pathList['body_2']).extract()
         if(bodyList and self._page<2):
             self._page+=1
             for index,value in enumerate(bodyList):
                 try:
                     url=Selector(text=value).xpath('//div[1]/div[1]/a/@href').extract()[0]
                     _url='https:'+url
                     yield scrapy.Request(url=_url,callback=self.page)
                 except:
                      print('parse is error')

             #_url='https://www.aliexpress.com/store/1495459/search/'+str(self._page)+'.html?spm=2114.12010615.0.0.49fee69faWBLxR&origin=n&SortType=bestmatch_sort'
             _url='https://shein.aliexpress.com/store/1159363/search/'+str(self._page)+'.html?spm=2114.12010615.0.0.56721044xPMPBJ&origin=n&SortType=bestmatch_sort'
             bodyList=scrapy.Request(url=_url,callback=self.parse)
             yield bodyList

     def page(self,response):
             print('----========')
             print(response.status)
             pathList={'title':'//*[@id="j-product-detail-bd"]/div[1]/div/h1/text()',
                       'lowPrice':'//*[@id="j-sku-discount-price"]/span[1]/text()',
                       'hightPrice':'//*[@id="j-sku-discount-price"]/span[2]/text()',
                       'disCountPrice':'//*[@id="j-sku-discount-price"]/text()',#有单价就没高低价
                       'scriptBigImg':'//*[@id="j-detail-gallery-main"]/script/text()',#幻灯片大图
                       'scriptMainImg':'//*[@id="j-detail-gallery-main"]/script/text()',#幻灯片主图
                       'contents':'//*[@id="j-product-description"]/div[2]/div/text()',
                       'orders':'//*[@id="j-order-num"]',
                       'objectId':'//*[@id="buy-now-form"]/input[1]/@value'
                       }
             item=smtconfig()
             if(not bool(response.selector.xpath(pathList['title']).extract())):
                 yield scrapy.Request(url=response.url,callback=self.page)
             else:
                 f=open('body2.text','w')
                 f.write(response.body)
                 f.close()
                 title=response.selector.xpath(pathList['title']).extract()[0]
                 item['title']=title.encode('utf-8')
                 try:
                     lowPrice=response.selector.xpath(pathList['lowPrice']).extract()[0]
                     item['lowPrice']=float(lowPrice.encode('utf-8'))
                     item['hightPrice']=hightPrice=float(response.selector.xpath(pathList['hightPrice']).extract()[0].encode('utf-8'))
                     item['disCountPrice']=0.00
                 except:
                     item['disCountPrice']=disCountPrice=float(response.selector.xpath(pathList['disCountPrice']).extract()[0].encode('utf-8'))
                     item['lowPrice']=0.00
                     item['hightPrice']=0.00
                 scriptBigImg=response.selector.xpath(pathList['scriptBigImg']).extract()[0].replace('\r','').replace('\n','').replace('\t','')
                 item['scriptBigImg']=_scriptBigImg= re.search(r'imageBigViewURL=\[(.*?)\]\;',scriptBigImg).group(1).encode('utf-8').strip('"')#主图幻灯
                 item['scriptMainImg']=_scriptBigMainImg= re.search(r'mainBigPic = (.*?)\;',scriptBigImg).group(1).encode('utf-8').strip('"')#主图
                 item['itemSpecifics']=self.specifics(response.body)
                 item['objectId']=response.selector.xpath(pathList['objectId']).extract()[0].encode('utf-8')
                 sku=self.sku(response.body)
                 item['itemSku']=sku['totalJson']
                 item['itemBigPic']=sku['skuBigPic']
                 item['skuKey']=sku['skuKey']
                 item['skuValue']=sku['skuValue']
                 item['orders']=orders=re.compile('\d+').findall(response.selector.xpath(pathList['orders']).extract()[0])[0].encode('utf-8')
                 item['originalUrl']=response.url
                 yield item


     def specifics(self,response):
         total={}
         speciRule={'div':'//*[@id="j-product-desc"]/div[1]/div[2]/ul/li','spKey':'//span[2]/text()','spValue':'//span[1]/text()'}
         ifSpecis=bool(Selector(text=response).xpath(speciRule['div']).extract())
         if(ifSpecis):
             for value in Selector(text=response).xpath(speciRule['div']).extract():
                 spkey=Selector(text=value).xpath(speciRule['spKey']).extract()[0]
                 spValue=Selector(text=value).xpath(speciRule['spValue']).extract()[0]
                 total.setdefault(spValue,spkey)
             return json.dumps(total)


     def sku(self,response):
         # //*[@id="j-product-info-sku"]
         # //*[@id="j-sku-list-1"]
         # //*[@id="j-sku-list-2"]
          regRules={'sku':'//*[@id="j-product-info-sku"]/dl','sku_name':'//dt/text()','sku_value':'//dd/ul/li','sku_a_attr':'//a/@title',
                    'sku_span_attr':'//a/span/text()','sku_big_pic':'//a/img/@bigpic'}
          ifSku=bool(Selector(text=response).xpath(regRules['sku']).extract())
          total={}
          kk=0
          skuKey=[]
          skuValue=[]
          skuJoinKeyAndValue={}
          lskuName={}
          skuBigPic=''
          if(ifSku==True):
              for value in Selector(text=response).xpath(regRules['sku']).extract():
                  skuAttr=''
                  skuName=Selector(text=value).xpath(regRules['sku_name']).extract()[0]
                  lskuName[skuName]=[]
                  for liValue in Selector(text=value).xpath(regRules['sku_value']).extract():
                      if(bool(Selector(text=liValue).xpath(regRules['sku_a_attr']).extract())):
                          skuAttr=Selector(text=liValue).xpath(regRules['sku_a_attr']).extract()[0]
                          if kk==0:
                             skuKey.append(skuAttr)
                          if kk==1:
                              skuValue.append(skuAttr)
                      else:
                          if(bool(Selector(text=liValue).xpath(regRules['sku_span_attr']).extract())):
                              skuAttr=Selector(text=liValue).xpath(regRules['sku_span_attr']).extract()[0]
                              if kk==0:
                                 skuKey.append(skuAttr)
                              if kk==1:
                                 skuValue.append(skuAttr)
                      if(bool(Selector(text=liValue).xpath(regRules['sku_big_pic']).extract())):
                          skuBigPic+=Selector(text=liValue).xpath(regRules['sku_big_pic']).extract()[0]+','
                      lskuName[skuName].append(skuAttr)

                  total.update(lskuName)
                  kk+=1
              # if(len(skuKey)>0):
              #     for ii in skuKey:
              #         if(len(skuValue)>0):
              #             for iii in skuValue:
              #                 skuJoinKeyAndValue.update(str(ii),str(iii))
              #         else:
              #             skuJoinKeyAndValue.update(str(ii),'')
              return {'totalJson':json.dumps(total),'skuBigPic':str(skuBigPic.rstrip(',')),'skuKey':skuKey,'skuValue':skuValue}

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























