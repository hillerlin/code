import redis
from error import PoolEmptyError
from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
import random


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        if REDIS_PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=REDIS_PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        get proxies from redis
        """
        proxies = self._db.lrange("proxies", 0, -1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        self._db.rpush("proxies", proxy)

    def pop(self):
        """
        get proxy from right.
        """
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    def randomChoic(self,index=1):
        count=self._db.llen("proxies")-1
        try:
            _count=random.randint(0,count)
            return self._db.lrange("proxies", _count, _count)[0].decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
