# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup


class MytestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    #title=scrapy.Field();
    singleUrl=scrapy.Field();#单品链接
    singleDes=scrapy.Field();#单品描述
    singleImg=scrapy.Field();#单品图片链接
    singleTitle=scrapy.Field();#单品标题
    singleArea=scrapy.Field();#单品地区
    singleId=scrapy.Field();#单品id
    singleRareTotalRe=scrapy.Field();#单品好评总数
    singleGradeAvge=scrapy.Field();#单品指数
    singlePicNum=scrapy.Field();#单品晒单总数
    singleUsed=scrapy.Field();#单品追加总数

class Yindouwang(scrapy.Item):
    pro_name=scrapy.Field();#项目名称
    pro_rate=scrapy.Field();#项目利率
    pro_limit=scrapy.Field();#项目期限
    pro_start_time=scrapy.Field();#项目期限
    pro_end_time=scrapy.Field();#项目期限
    pro_price=scrapy.Field();#项目期限
    pro_type_dsc=scrapy.Field();#项目期限
    user_name=scrapy.Field();#项目期限
    user_bid_price=scrapy.Field();#项目期限
    user_buy_time=scrapy.Field();#项目期限
    user_bid_type=scrapy.Field();#项目期限
    pro_id=scrapy.Field();#项目期限
    user_record_list=scrapy.Field();#项目期限
class liyedaiProduct(scrapy.Item):
    pro_name=scrapy.Field();#项目名称
    pro_rate=scrapy.Field();#项目利率
    pro_limit=scrapy.Field();#项目期限
    pro_start_time=scrapy.Field();#项目期限
    pro_end_time=scrapy.Field();#项目期限
    pro_price=scrapy.Field();#项目期限
    pro_type_dsc=scrapy.Field();#项目期限
    pro_id=scrapy.Field();#项目期限
    user_record_list=scrapy.Field();#项目期限
    user_name=scrapy.Field();#项目期限
    user_bid_price=scrapy.Field();#项目期限
    user_buy_time=scrapy.Field();#项目期限
    user_bid_type=scrapy.Field();#项目期限
class smtconfig(scrapy.Item):
    title=scrapy.Field();
    lowPrice=scrapy.Field();
    hightPrice=scrapy.Field();
    disCountPrice=scrapy.Field();
    scriptBigImg=scrapy.Field();
    scriptMainImg=scrapy.Field();
    contents=scrapy.Field();
    itemSpecifics=scrapy.Field();
    itemSku=scrapy.Field();
    orders=scrapy.Field();
    originalUrl=scrapy.Field();






