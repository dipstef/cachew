import os
import quiche
from quiche.cache import HttpResponseCached
from quiche.client import CacheOrClient
from softarchive.util.httpy_retry import HttpClient


def main():
    cache_path = os.path.join(os.path.dirname(__file__), 'cache.db')

    try:
        cache = quiche.connect(cache_path)

        client_cache = CacheOrClient(cache, HttpClient())

        url = 'http://www.repubblica.it'

        response = client_cache.get(url)
        assert not isinstance(response, HttpResponseCached)
        retrieve_date = response.date

        response = client_cache.get(url)
        assert isinstance(response, HttpResponseCached)
        assert response.date == retrieve_date

    finally:
        if os.path.exists(cache_path):
            os.remove(cache_path)


if __name__ == '__main__':
    main()