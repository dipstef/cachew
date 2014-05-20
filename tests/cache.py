import os
from httpy import cache as httpy_cache
from httpy.cache.cache import HttpResponseCached
from httpy.cache.client import ClientOrCache
from softarchive.util.httpy_retry import HttpClient


def main():
    cache_path = os.path.join(os.path.dirname(__file__), 'cache.db')

    try:
        cache = httpy_cache.connect(cache_path)

        client_cache = ClientOrCache(HttpClient(), cache)

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