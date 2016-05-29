import cPickle as pickle
import hashlib
from cStringIO import StringIO
from contextlib import closing
from datetime import datetime
from httpy import HttpHeaders, HttpResponse

from pysqlite2 import dbapi2 as sqlite3
from urlo.normalize import unquoted

from .cache_db import get_response, insert_response, update_response, get_history, insert_history


class SqlLiteCache(closing):
    def __init__(self, conn):
        """ :type conn: quelo.sqlite.DbFile"""
        super(SqlLiteCache, self).__init__(self)
        self._conn = conn
        self._cursor = self._conn.cursor()

    def get(self, request):
        response = get_response(self._cursor, unquoted(request.url), request.method)
        if response:
            response = _create_response(request, *response)
            return response

    def store(self, response, keep_history=True):
        self._insert_response(response.request, response, keep_history=keep_history)
        self._conn.commit()

    def _insert_response(self, request, response, keep_history=True):
        request_url = unquoted(request.url)
        response_url = unquoted(response.url)
        headers_dict = dict(response.headers)
        headers = pickle.dumps(headers_dict)
        body = sqlite3.Binary(response.body)

        previous = get_response(self._cursor, request_url, request.method)
        if not previous:
            self._insert(request_url, request.method, response_url, response.status, response.date, headers, body)
        else:
            self._update(request_url, request.method, response_url, response.status, response.date, headers, body)
            if keep_history:
                self._save_history(request_url, request.method, *previous)

    def _insert(self, request_url, method, response_url, status, date, headers, body):
        insert_response(self._cursor, request_url, method, response_url, status, date, headers, body)

    def _update(self, request_url, method, response_url, status, date, headers, body):
        update_response(self._cursor, request_url, method, response_url, status, date, headers, body)

    def _save_history(self, url, method, response_url, status, headers, body, date):
        body_str = str(body)

        sha1 = _checksum(StringIO(body_str))

        unchanged = get_history(self._cursor, url, method, sha1)
        if not unchanged:
            body = sqlite3.Binary(body_str)
            insert_history(self._cursor, url, method, sha1, response_url, status, date, headers, body)

    def close(self):
        self._cursor.close()
        self._conn.close()


def _create_response(request, url, status, headers, body, response_date):
    return CachedHttpResponse(request, url, int(status), pickle.loads(str(headers)), str(body), response_date)


def _checksum(buf, block_size=1024 * 128):
    sha1 = hashlib.sha1()

    for chunk in iter(lambda: buf.read(block_size), b''):
        sha1.update(chunk)
    return sha1.hexdigest()


class CachedHttpResponse(HttpResponse):
    def __init__(self, request, url, status, headers, body, date):
        super(CachedHttpResponse, self).__init__(request, url, status, HttpHeaders(headers), body)
        self.date = date
        self.flags = ['cached']

    def is_older_than(self, expiration):
        return expiration and datetime.utcnow() - self.date >= expiration
