import time
from multiprocessing import Process
import asyncio
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError
from proxypool.getter import FreeProxyGetter
from proxypool.setting import *
from asyncio import TimeoutError
from .agents import AGENTS
from random import choice


class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []


    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    def set_timing_params(self):
        self._conn = RedisClient()
        self._all_ips_item=self._conn.getAll() #把现在所有的ip列表都拿出来做检查
        self._post_url=ALIE_API

    async def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(self.test_api, proxy=real_proxy, timeout=get_proxy_timeout) as response:
                        if response.status == 200:
                            self._conn.put(proxy)
                            print('Valid proxy', proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Invalid proxy', proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
            print(s)
            pass

    def test(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]#test_single_proxy  检验ip是否有效
            loop.run_until_complete(asyncio.wait(tasks))
            #loop.run_until_complete(asyncio.gather(self.test_single_proxy(proxy) for proxy in self._raw_proxies))
        except ValueError:
            print('Async Error')

    async def TimingCheckFunction(self,proxy):
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy,bytes):#bytes=str
                        proxy=proxy.decode('utf-8')
                    real_proxy='http://'+proxy
                    headers = {'User-Agent':choice(AGENTS)}
                    print('Timing Check Async Ip:'+str(proxy))
                    async with session.get(self._post_url, proxy=real_proxy, timeout=get_proxy_timeout,headers=headers) as response:
                        if(response.status!=200):
                            self._conn.delete(proxy)
                            print('Delete Old Invalid Proxy',proxy)
                        else:
                            print('Keep Save IP',proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Foreach Delete Invalid Proxy Error', proxy)
                    self._conn.delete(proxy)
        except(ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
            print('-------')
            print(s)
            #self._conn.delete(proxy)
            pass

    def TimingCheck(self):
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.TimingCheckFunction(proxy) for proxy in self._all_ips_item]#test_single_proxy  检验ip是否有效
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('Timing Check Error')



class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)  #赋值
                self._tester.test() #接着上一步的赋值检验ip
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


class Schedule(object):
    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        """
        Get half of proxies which in redis
        """
        conn = RedisClient()
        tester = ValidityTester()
        while True:
            print('Refreshing ip')
            count = int(0.5 * conn.queue_len)
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
        If the number of proxies less than lower_threshold, add proxy
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def timingCheck(cycle=TIMING_CHECK):
        conn = RedisClient()
        valiClass=ValidityTester()
        while True:
               if conn.queue_len>0:
                   valiClass.set_timing_params()
                   valiClass.TimingCheck()
               time.sleep(cycle)


    def run(self):
        print('Ip processing running')
        valid_process = Process(target=Schedule.valid_proxy)
        check_process = Process(target=Schedule.check_pool)
        timing_check_process=Process(target=Schedule.timingCheck)
        valid_process.start()
        check_process.start()
        timing_check_process.start()
