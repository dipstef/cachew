Quiche
======

``sqlite`` http response cache.


Usage
=====

.. code-block:: python

    import cachew
    from httpy import httpy

    with cachew.connect('cache.db') as cache:
        response = httpy.get('http://www.google.com')
        cache.store(response)

        response = cache.get('http://www.google.com')
        assert isinstance(response, cachew.CachedHttpResponse)


Can be used transparently with an http client, to retrieve responses already cached or store un-existing ones or expired

.. code-block:: python

    from cachew import CacheOrClient

    >>> cache = CacheOrClient(cache, httpy)

    >>> response = cache.get('http://www.google.com')
    >>> cache_response = cache.get(url)
    assert cache_response.date == response.date


Expiration

.. code-block:: python

    >>> response = cache.get('http://www.google.com', expiration=seconds(1))

Force client retrieval

.. code-block:: python

    >>> response = cache.get('http://www.google.com', force_refresh=True)



