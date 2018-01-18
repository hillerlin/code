import json
from mytest.db import RedisClient
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

redis=RedisClient();
list=redis.get()
def _pr(i):
  print(i)
def __pr(i):
  print(i+'--')

[_pr(i) for i in redis.get()]
[__pr(i) for i in redis.get()]