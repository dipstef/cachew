import os
from dated.timedelta import seconds

from httpy import httpy

import quiche
from quiche.cache import CachedHttpResponse
from quiche import CacheOrClient


def main():
    try:
        with quiche.connect('cache.db') as cache:

            client_cache = CacheOrClient(cache, httpy)

            url = 'http://www.google.com'

            response = client_cache.get(url)
            assert not isinstance(response, CachedHttpResponse)
            retrieve_date = response.date

            response = client_cache.get(url)
            assert isinstance(response, CachedHttpResponse)
            assert response.date == retrieve_date

            response = client_cache.get(url, expiration=seconds(1))
            assert not isinstance(response, CachedHttpResponse)
    finally:
        if os.path.exists('cache.db'):
            os.remove('cache.db')


if __name__ == '__main__':
    main()