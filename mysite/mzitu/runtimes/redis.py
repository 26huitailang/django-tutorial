#!/usr/bin/python
# coding: utf-8

import redis
from django.conf import settings


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        # The default connection parameters are: host='localhost', port=6379, db=0
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


class PicJsonRedis(object):
    """pic存于redis中的数据结构"""

    def __init__(self, full_path=None, url=None, header_referer=None, suite_url=None):
        self.full_path = full_path
        self.url = url
        self.header_referer = header_referer
        self.suite_url = suite_url  # 后面用于查找外键


mzitu_image_queue = RedisQueue('mzitu_image', host=settings.REDIS_HOST)
mzitu_url_queue = RedisQueue('mzitu_url', host=settings.REDIS_HOST)
