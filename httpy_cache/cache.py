import cPickle as pickle
from contextlib import closing

from httpy.headers import HttpHeaders
from httpy.response import HttpResponse
from pysqlite2 import dbapi2 as sqlite3
from urlo.normalize import unquoted

from .cache_db import get_response, insert_response, update_response


class SqlLiteCache(closing):
    def __init__(self, conn):
        super(SqlLiteCache, self).__init__(self)
        self._conn = conn
        self._cursor = self._conn.cursor()

    def get_response(self, request):
        response = get_response(self._cursor, unquoted(request.url), request.method)
        if response:
            response = _create_response(request, *response)
            return response

    def store(self, response):
        self._insert_response(response.request, response)
        self._conn.commit()

    def _insert_response(self, request, response):
        request_url = unquoted(request.url)
        response_url = unquoted(response.url)
        headers_dict = dict(response.headers)
        headers = pickle.dumps(headers_dict)
        body = sqlite3.Binary(response.body)

        self._insert_or_update(request_url, request.method, response_url, response.status, response.date, headers, body)

    def _insert_or_update(self, request_url, method, response_url, status, date, headers, body):
        response_in_cache = get_response(self._cursor, request_url, method)

        if not response_in_cache:
            insert_response(self._cursor, request_url, method, response_url, status, date, headers, body)
        else:
            update_response(self._cursor, request_url, method, response_url, status, date, headers, body)

    def close(self):
        self._cursor.close()
        self._conn.close()


def _create_response(request, url, status, headers, body, response_date):
    return HttpResponseCached(request, url, int(status), pickle.loads(str(headers)), str(body), response_date)


class HttpResponseCached(HttpResponse):
    def __init__(self, request, url, status, headers, body, date):
        super(HttpResponseCached, self).__init__(request, url, status, HttpHeaders(headers), body)
        self.date = date
        self.flags = ['cached']