# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import time
from hashlib import md5
from items import smtconfig
# class MytestPipeline(object):
#     def __init__(self):
#         host=settings['MONGODB_HOST']
#         port=settings['MONGODB_PORT']
#         dbname=settings['MONGODB_DBNAME']
#         tablename=settings['MONGODB_DOCNAME']
#         client=pymongo.MongoClient(host=host,port=port)
#         tdb=client[dbname]
#         self.post=tdb[tablename]
#     def process_item(self, item, spider):
#         shopInfo=dict(item)
#         self.post.insert(shopInfo)
#         return item
class MytestPipeline(object):
    def process_item(self,item,spider):
        return item
def from_settings(settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return dbpool


class MySQLStorePipelinetest(object):
       def process_item(self,item,spider):
           #if(isinstance(item,smtconfig)):
               #print(item['pro_id'])
           # elif(isinstance(item,liyedaiUser)):
           #     print(item['user_bid_price'])
           return item
class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool=from_settings(settings);
    #pipeline默认调用
    def process_item(self,item,spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return item
        #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        #linkmd5id = self._get_linkmd5id(item)
        #now = ''#datetime.utcnow().replace(microsecond=0).isoformat(' ')
        # conn.execute("""
        # insert into `yindouwang_project`(`pro_name`,`pro_id`,`pro_limit`,`pro_rate`,`pro_start_time`,`pro_end_time`,`pro_price`,`pro_type_dsc`)
        # VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')
        # """%(item['pro_name'],item['pro_id'],item['pro_limit'],item['pro_rate'],item['pro_start_time'],item['pro_end_time'],item['pro_price'],item['pro_type_dsc']))
        # for index,value in enumerate(item['user_record_list']):
        #     conn.execute("""
        #     insert into `yindouwang_user_record` (`user_name`,`user_bid_price`,`user_buy_time`,`pro_id`) VALUES
        #     ('%s','%s','%s','%s')"""%(value['user_name'],value['user_bid_price'],value['user_buy_time'],value['pro_id']))
        print('--------begin')
        print(item)
        print('--------end')
        #conn.execute("""insert into `yindouwang_project`(`pro_name`,`pro_id`) VALUES ('%s',%d) """%('aaaa',9090))
        conn.execute("""
                     insert into `smt`(`title`,`low_price`,`hight_price`,`dis_count_price`,`script_main_img`,`script_big_img`) VALUES ('%s',%f,%f,%f,'%s','%s')
                     """%(item['title'],item['lowPrice'],item['hightPrice'],item['disCountPrice'],item['scriptMainImg'],item['scriptBigImg']))
    #获取url的md5编码
    def _get_linkmd5id(self, item):
            #url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()
        #异常处理
    def _handle_error(self, failue, item, spider):
        print(failue)
    def timeTostring(self,_time):
        return time.mktime(time.strftime(_time,'%Y-%m-%d %H:%M:%S'))
