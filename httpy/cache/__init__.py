import os

from httpy.request import HttpRequest

from .cache import SqlLiteCache


class PageResponseCache(object):

    def __init__(self, cache):
        self._cache = cache

    def get_response(self, url, method='GET'):
        request = HttpRequest(url, method=method)
        return self._cache.get_response(request)

    def store(self, response):
        self._cache.store(response)

    def close(self):
        self._cache.close()

    def __getattr__(self, method):
        return lambda url: self.get_response(url, method.upper())


_init_file = os.path.join(os.path.dirname(__file__), 'cache.sql')


class CacheConnect(object):

    def __init__(self, connection):
        self._connection = connection

    def __call__(self, path, **kwargs):
        conn = self._connection(path, init_file=_init_file, **kwargs)
        return SqlLiteCache(conn)