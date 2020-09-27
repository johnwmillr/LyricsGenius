.. _other_guides:

Other Guides
============


Request Errors
--------------
The package will raise all HTTP and timeout erros using
the ``HTTPError`` and ``Timeout`` classes of the
``requests`` package. Whenever an HTTP error is raised,
proper description of the error will be printed to
output. You can also access the response's status code.

.. code:: python
    
    from requests.exceptions import HTTPError, Timeout
    from lyricsgenius import Genius

    try:
        Genius('')
    except HTTPError as e:
        print(e.errno)    # status code
        print(e.args[0])  # status code
        print(e.args[1])  # error message
    except Timeout:
        pass
