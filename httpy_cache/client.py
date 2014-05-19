class ClientOrCache(object):

    def __init__(self, client, cache):
        self._client = client
        self._cache = cache

    def get(self, url, headers=None, force_refresh=False, **kwargs):
        if force_refresh:
            response = self._get_client_response(url, headers, **kwargs)
        else:
            response = self._get_cache_response(url) or self._get_client_response(url, headers)

        return response

    def _get_cache_response(self, url):
        response = self._cache.get_response(url)
        if response:
            return response

    def _get_client_response(self, url, headers, **kwargs):
        response = self._client.get(url, headers=headers, **kwargs)

        self._cache.store(response)
        return response

    def post(self, url, data=None, headers=None, **kwargs):
        response = self._client.post(url, data=data, headers=headers, **kwargs)

        self._cache.store(response)
        return response