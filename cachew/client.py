from httpy import httpy


class CacheOrClient(object):

    def __init__(self, cache, client=httpy):
        self._cache = cache
        self._client = client

    def get(self, url, headers=None, force_refresh=False, expiration=None, **kwargs):
        if force_refresh:
            response = self._get_client_response(url, headers, **kwargs)
        else:
            response = self._get_cache_response(url, expiration) or self._get_client_response(url, headers)

        return response

    def _get_cache_response(self, url, expiration=None):
        response = self._cache.get_response(url)
        if response and not response.is_older_than(expiration):
            return response

    def _get_client_response(self, url, headers, **kwargs):
        response = self._client.get(url, headers=headers, **kwargs)

        self._cache.store(response)
        return response

    def post(self, url, data=None, headers=None, **kwargs):
        response = self._client.post(url, data=data, headers=headers, **kwargs)

        self._cache.store(response)
        return response