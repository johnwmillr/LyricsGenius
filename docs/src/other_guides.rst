.. _other_guides:

Other Guides
============


Request Errors
--------------
The package will raise all HTTP and timeout errors using
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


Logging
-------
LyricsGenius uses Python's ``logging`` module to log
relevant messages including the progress of searching
for a song and much more. If you use LyricsGenius from
the command line, just add the ``--verbose`` parameter.
Otherwise, follow this example:

.. code:: python

    import logging

    from lyricsgenius import Genius

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("lyricsgenius")
    logger.setLevel(logging.INFO)

    genius = Genius(GENIUS_ACCESS_TOKEN)
    song = genius.search_song("To You", "Andy Shauf")
