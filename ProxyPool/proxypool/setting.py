# Redis数据库的地址和端口
HOST = '59.110.136.193'
PORT = 6600

# 如果Redis有密码，则添加这句密码，否则设置为None或''
PASSWORD = 'lmj4282887'

# 获得代理测试时间界限
get_proxy_timeout = 9

# 代理池数量界限
POOL_LOWER_THRESHOLD = 200
POOL_UPPER_THRESHOLD = 600

# 检查周期
VALID_CHECK_CYCLE = 30
POOL_LEN_CHECK_CYCLE = 20
#实时检查周期
TIMING_CHECK=5

# 测试API，用百度来测试
TEST_API='http://www.baidu.com'
ALIE_API='https://www.aliexpress.com'