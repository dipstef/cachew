Quiche
======

``sqlite`` http response cache.


Usage
=====

.. code-block:: python

    import quiche
    from httpy import httpy

    with quiche.connect('cache.db') as cache:

        response = cache.get_response(url)
        if not response:
            response = httpy.get('http://www.google.com')
            cache.store(response)
            response = cache.get_response('http://www.google.com')
        assert isinstance(response, quiche.CachedHttpResponse)


Can be used transparently with an http client, to retrieve responses already cached or store un-existing ones or expired

.. code-block:: python

    from quiche import CacheOrClient

    >>> client_cache = CacheOrClient(cache, httpy)

    >>> response = client_cache.get('http://www.google.com')
    assert not isinstance(response, CachedHttpResponse)
    retrieve_date = response.date

    >>> response = client_cache.get(url)
    assert isinstance(response, CachedHttpResponse)
    assert response.date == retrieve_date


Expiration

.. code-block:: python

    >>> response = client_cache.get('http://www.google.com', expiration=seconds(1))
    assert not isinstance(response, CachedHttpResponse)

Force client retrieval

.. code-block:: python

    >>> response = client_cache.get('http://www.google.com', force_refresh=True)
    assert not isinstance(response, CachedHttpResponse)



