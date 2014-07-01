from contextlib import closing
import os
import quelo
from httpy import HttpRequest
from .client import CacheOrClient
from .cache import SqlLiteCache


class PageResponseCache(closing):

    def __init__(self, cache):
        super(PageResponseCache, self).__init__(self)
        self._cache = cache

    def get_response(self, url, method='GET'):
        request = HttpRequest(method, url)
        return self._cache.get_response(request)

    def store(self, response):
        self._cache.store(response)

    def close(self):
        self._cache.close()

    def __getattr__(self, method):
        return lambda url: self.get_response(url, method.upper())


_init_file = os.path.join(os.path.dirname(__file__), 'cache.sql')


class CacheConnect(object):

    def __init__(self, connection=quelo.connect):
        self._connection = connection

    def __call__(self, path, **kwargs):
        conn = self._connection(path, init_file=_init_file, **kwargs)
        return PageResponseCache(SqlLiteCache(conn))


connect = CacheConnect(connection=quelo.connect)