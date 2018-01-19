import json
from mytest.db import RedisClient
import random
import MySQLdb
a='color'
aa='red'
aaa='green'
aaaa='blue'
b='size'
bb='x'
bbb='xx'
bbbb='xxl'

total={}
_a={}
_a['color']=[]
_a['color'].append('a')
_a['color'].append('b')
_b={}
_a['size']=[]
_a['size'].append('X')
_a['size'].append('XX')
_a['size'].append('XXL')

# total.update(_a)
# total.update(_a)
#print(json.dumps(_a))
# db=MySQLdb.connect('127.0.0.1','root','','scrapy')
# cursor=db.cursor()
# _insert='{"Gender:": "Men", "Sleeve Style:": "O sleeve", "Sleeve Length(cm):": "Full", "Item Type:": "Tops", "Sale by Pack:": "No", "Fit:": "Fits smaller than usual. Please check this store\'s sizing info", "Pattern Type:": "Solid", "Collar:": "Turn-down Collar", "Tops Type:": "Tees", "Model Number:": "TD-WHFE-022-1", "Hooded:": "No", "Brand Name:": "TACVASEN", "Style:": "Military", "Material:": "Cotton,Polyester", "Fabric Type:": "Broadcloth"}'
# sql="""INSERT INTO `smt` (`title`) VALUES ('%s')"""%(MySQLdb.escape_string(_insert))
# bb=cursor.execute(sql)
# db.close()
redis=RedisClient()
list=redis.get()
if '120.24.230.217:80881' not in list:
    print(1111)
