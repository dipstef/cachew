from contextlib import closing
import os
import quelo
from httpy import HttpRequest
from .client import CacheOrClient
from .cache import SqlLiteCache, CachedHttpResponse


class PageResponseCache(closing):

    def __init__(self, cache):
        """ :type cache: SqlLiteCache """
        super(PageResponseCache, self).__init__(self)
        self._cache = cache

    def get(self, url, method='GET'):
        return self._get_response(method, url)

    def _get_response(self, method, url):
        request = HttpRequest(method, url)
        return self._cache.get(request)

    def store(self, response):
        self._cache.store(response)

    def close(self):
        self._cache.close()

    def __getattr__(self, method):
        return lambda url: self._get_response(method.upper(), url)


_init_file = os.path.join(os.path.dirname(__file__), 'cache.sql')


class CacheConnect(object):

    def __init__(self, connection=quelo.connect):
        """:type connection: quelo.DbPathConnect
        """
        self._connection = connection

    def __call__(self, path, **kwargs):
        conn = self._connection(path, **kwargs)

        with open(_init_file) as fp:
            conn.execute_script(fp.read())
            conn.commit()

        return PageResponseCache(SqlLiteCache(conn))


connect = CacheConnect(connection=quelo.connect)
