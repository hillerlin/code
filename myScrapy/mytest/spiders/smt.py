# coding=utf-8
import scrapy
import re
#from bs4 import BeautifulSoup
import urllib2
from scrapy.http import Request
from scrapy import Selector
from ..items import smtconfig
#import json
import sys
import chardet
#import io
import time
reload(sys)
sys.setdefaultencoding('utf-8')

class smt(scrapy.Spider):
     name="smt"
     handle_httpstatus_list=[404,500]
     _page=1
     allowed_domains=['aliexpress.com']
     start_urls=[
            #"https://www.aliexpress.com/store/3026024/search/2.html?spm=2114.12010615.0.0.e119e1afYcSu2&origin=n&SortType=bestmatch_sort",
            #"https://www.aliexpress.com/store/all-wholesale-products/1752153.html?spm=2114.12010608.0.0.5597e5c58EqJzh",
            #"https://www.aliexpress.com/store/1752153/search/2.html?spm=2114.12010615.0.0.690106dcnzkT0h&origin=n&SortType=bestmatch_sort",
            #"https://www.aliexpress.com/store/1752153/search/3.html?spm=2114.12010615.0.0.2441392BI1oQy&origin=n&SortType=bestmatch_sort",

     ]

     def start_requests(self):
          yield scrapy.Request(url="https://www.aliexpress.com/item/TACVASEN-Army-Camouflage-Coat-Military-Tactical-Jacket-men-Soft-Shell-Waterproof-Windproof-Jacket-Coat-Plus-Size/32793996367.html?spm=2114.search0103.3.1.40ab65d5IjMGvZ&ws_ab_test=searchweb0_0,searchweb201602_2_10152_10151_10065_10068_10344_10342_10546_10343_10325_10340_10548_10341_10084_10083_10307_10615_10059_10314_10534_100031_10604_10103_10142,searchweb201603_6,ppcSwitch_5&algo_expid=c6742f30-ec0d-4c20-88a0-53d0abe3a23a-0&algo_pvid=c6742f30-ec0d-4c20-88a0-53d0abe3a23a&priceBeautifyAB=4",
                               callback=self.logged_in)

     def logged_in(self, response):
          f = open("body.txt",'a')
          f.write(response.body+'\n')
          f.close()

     def parse(self,response):
         totalPage=176
         # test1='window.runParams.imageBigViewURL=["https://ae01.alicdn.com/kf/HTB1cC8TSXXXXXcMaXXXq6xXFXXXW/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg","https://ae01.alicdn.com/kf/HTB1svDnh8fH8KJjy1Xbq6zLdXXaO/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg","https://ae01.alicdn.com/kf/HTB1HW3shY_I8KJjy1Xaq6zsxpXaJ/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg","https://ae01.alicdn.com/kf/HTB1Dx7fcLfM8KJjSZPfq6zklXXaN/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg","https://ae01.alicdn.com/kf/HTB11Y22h4rI8KJjy0Fpq6z5hVXaZ/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg","https://ae01.alicdn.com/kf/HTB12FQxXTwKL1JjSZFgq6z6aVXaJ/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg"];window.runParams.mainBigPic = "https://ae01.alicdn.com/kf/HTB1cC8TSXXXXXcMaXXXq6xXFXXXW/0-2gnail-neon-aurora-pigement-Unicorn-Nail-Powder-Mermaid-Nail-Art-Chrome-Pigment-Manicure-Decorations-in.jpg";'
         # #m = re.match(r'who(.*?)thereis', 'who you are,what you do,When you get get there? What is time you state thereis?')
         # m = re.search(r'imageBigViewURL=\[(.*?)\]\;', test1)
         # print('---------------')
         # #print "m.string:", m.string
         # print(m.group(1))
         # pass
         # exit
         pathList={'body':'//*[@id="list-items"]/ul/li','body_2':'//*[@id="node-gallery"]/div[5]/div/div/ul/li'}
         #body=response.body.decode('utf-8','ignore')
         #bodyList=Selector(text=body).xpath(pathList['body']).extract()
         bodyList=response.selector.xpath(pathList['body_2']).extract()
         # f = open("text14.txt",'a')
         # #f.write(body+'\n')
         # for p in bodyList:
         #     print('------------------')
         #     try:
         #         #url=Selector(text=p).xpath('//div/div[1]/div/a/@href').extract()[0]
         #         url=Selector(text=p).xpath('//div[1]/div[1]/a/@href').extract()[0]
         #         #//*[@id="node-gallery"]/div[5]/div/div/ul/li[1]/div[1]/div[1]/a
         #         f.write('-------------------------')
         #         f.write(url+'\n')
         #     except:
         #        print '-----code error'
         #
         # f.close()

         if(bodyList and self._page<2):
             self._page+=1
             for index,value in enumerate(bodyList):
                 try:
                     url=Selector(text=value).xpath('//div[1]/div[1]/a/@href').extract()[0]
                     _url='https:'+url
                     f = open("text15.txt",'a')
                     f.write(_url+'\n')
                     yield scrapy.Request(url=_url,callback=self.page)
                 except:
                     f.close()

             #
             # _url='https://www.yindou.com/zhaiquangoumai/?page='+str(self._page)+'&total=2802&rate=0&guarantee_id_code=&leftday=0&backday=0'
             # bodyList=scrapy.Request(url=_url,cookies={'PHPSESSID':'0pnglqi9n9q6ototh6skpslb67',
             #                               '__jsluid':'a8a08442bcb30fa94fcc184d0edd1619',
             #                               'gr_user_id':'dd9cb2dd-f8d8-430c-9ebd-d93f310f9450',
             #                               'ydrecord':'533220_1495088148',
             #                               'gr_session_id_b9a32bc6f5df5804':'ab02d7a9-5771-4db0-abcd-335892026d61'},
             #             callback=self.parse)
             # yield bodyList

     def page(self,response):
         if response.status in self.handle_httpstatus_list:
            print("maincoming page is wrong!")
            pass
         else:
             pathList={'title':'//*[@id="j-product-detail-bd"]/div[1]/div/h1/text()',
                       'lowPrice':'//*[@id="j-sku-discount-price"]/span[1]/text()',
                       'hightPrice':'//*[@id="j-sku-discount-price"]/span[2]/text()',
                       'disCountPrice':'//*[@id="j-sku-discount-price"]/text()',#有单价就没高低价
                       'scriptBigImg':'//*[@id="j-detail-gallery-main"]/script/text()',#幻灯片大图
                       'scriptMainImg':'//*[@id="j-detail-gallery-main"]/script/text()',#幻灯片主图
                       'contents':'//*[@id="j-product-description"]/div[2]/div/text()',
                       }
             item=smtconfig()
             title=response.selector.xpath(pathList['title']).extract()[0]
             item['title']=title.encode('utf-8')
             #write=''
             try:
                 lowPrice=response.selector.xpath(pathList['lowPrice']).extract()[0]
                 item['lowPrice']=float(lowPrice.encode('utf-8'))
                 item['hightPrice']=hightPrice=float(response.selector.xpath(pathList['hightPrice']).extract()[0].encode('utf-8'))
                 item['disCountPrice']=0.00
                 #write=title+lowPrice+'__'+hightPrice+'__'+'\n'
             except:
                 item['disCountPrice']=disCountPrice=float(response.selector.xpath(pathList['disCountPrice']).extract()[0].encode('utf-8'))
                 item['lowPrice']=0.00
                 item['hightPrice']=0.00
                 #write=title+disCountPrice+'\n'
             scriptBigImg=response.selector.xpath(pathList['scriptBigImg']).extract()[0].replace('\r','').replace('\n','').replace('\t','')
             item['scriptBigImg']=_scriptBigImg= re.search(r'imageBigViewURL=\[(.*?)\]\;',scriptBigImg).group(1).encode('utf-8')#主图幻灯
             item['scriptMainImg']=_scriptBigMainImg= re.search(r'mainBigPic = (.*?)\;',scriptBigImg).group(1).encode('utf-8')#主图
             #item['contents']=contents= response.selector.xpath(pathList['contents']).extract()[0]#内容
             #print(contents)
             # buyRecordList=response.selector.xpath(pathList['bidlist']).extract()
             # for index,value in enumerate(buyRecordList):
             #       user_name=Selector(text=value).xpath('//div/span[1]/text()').extract()[0]
             #       _user_bid_price=Selector(text=value).xpath('//div/span[2]/text()').re('(\d+\.\d+)|(\d+)')
             #       user_bid_price=_user_bid_price[0] if _user_bid_price[0] else _user_bid_price[1]
             #       user_buy_time=Selector(text=value).xpath('//div/span[3]/text()').extract()[0]
             #       recordList.append({'user_bid_price':user_bid_price,'user_name':user_name,'user_buy_time':self.timeTostring(user_buy_time,2),'pro_id':item['pro_id']})
             # item['user_record_list']=recordList
             yield item
             # body=response.body.decode('utf-8','ignore')
             # f = open("text14.txt",'a')
             # f.write(body+'\n')
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























