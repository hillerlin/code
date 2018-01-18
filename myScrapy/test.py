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

keys = ['a', 'b', 'c']
_keys=['A','B','C','D','E']
values = {'a':'b','a':'c'}
"'ali_apache_id=11.227.7.24.149474220428.932627.3; ali_beacon_id=11.227.7.24.149474220428.932627.3; cna=meSeEeRCNTgCAWUufFYTNOWA; __utma=3375712.1446485571.1515241418.1515241433.1515294697.2; __utmz=3375712.1515241433.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1446485571.1515241418; JSESSIONID=6E59B6953F4D6CB6376C93A08CC61AB9; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFSMnM1tXQyszQ1djNxMXN2MjM2N3O2NHY0sHB2NjN0dLJU0kkusTI0NTQzsjA3sjQGsnQSk9EEciusDGqjAJ9wF98%3D; xman_t=mBMdSxVaL6eLAk1PciVt7BoYfaK8FqyNXm9mhXkEOIBXkBfeZHJOVzVpRt5uyBXEonhMoMkmaj2NmtIRSQufIGp6lFr0qh0Q; xman_f=/tXrut2GDvwhZahXpRTRTyRZY2TLSkGczem/4JSPn5nrOCBOiysMbKmX4yCafm/ilxuC7IUkpolnWwVHJSrDi7y7HXsCJwCg6wRvdYClZqiV5ug+NBufDQ==; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932813066235%0932812958573%0932834464857%0932532472029%0932807812156%0932462970797%0932843620168%0932793996367; acs_usuc_t=acs_rt=d61368287e00439ca787e7b5dfdfd542&x_csrf=21vimh35z9me; _ym_uid=15163009971034512808; xman_us_f=x_l=1&x_locale=en_US; aep_usuc_f=region=US&site=glo&b_locale=en_US&c_tp=USD; intl_locale=en_US; intl_common_forever=FSvni10kaeo/WTvxrRb4EoIoxDTJxpLxkOmaQIeDavXq5tT61237ag==; isg=BKamDenPwFEG9pTFf30EDU-59xzoL-pFZVn5ZJBPkkmkE0Yt-Bc6UYzhbw2foOJZ; ali_apache_track" "" ali_apache_tracktmp='
# for ii in keys:
#   for iii in _keys:
#        values.update([(ii,iii)])
#        print(ii+iii)
print(values)