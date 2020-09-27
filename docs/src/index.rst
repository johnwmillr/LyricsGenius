.. _index:
.. image:: header.png


LyricsGenius: a Python client for the Genius.com API
====================================================
.. image:: https://travis-ci.org/johnwmillr/LyricsGenius.svg?branch=master
   :target: https://travis-ci.org/johnwmillr/LyricsGenius
.. image:: https://badge.fury.io/py/lyricsgenius.svg
   :target: https://pypi.org/project/lyricsgenius/
.. image:: https://img.shields.io/badge/python-3.x-brightgreen.svg
   :target: https://pypi.org/project/lyricsgenius/

`Genius.com`_ is a fun website. If you aren’t familiar with it, Genius hosts a
bunch of song lyrics and lets users highlight and annotate passages with
interpretations, explanations, and references. Originally called RapGenius.com
and devoted to lyrics from rap and hip-hop songs, the website now includes
lyrics and annotations from all genres of music. You can figure out what
`“Words are flowing out like endless rain into a paper cup”`_ from Across the
Universe really means, or what Noname was referring to when she said `“Moses
wrote my name in gold and Kanye did the eulogy”`_.

It’s actually not too difficult to start pulling data from the Genius website.
Genius is hip enough to provide a free application programming interface (API)
that makes it easy for nerds to programmatically access song and artist data
from their website. What the Genius API doesn’t provide, however,
is a way to download the lyrics themselves. With a little help from
`Beautiful Soup`_ though, it’s possible to grab the song lyrics without too
much extra work. And LyricsGenius has done all of that for you already.

..
   source::https://www.johnwmillr.com/scraping-genius-lyrics/


``lyricsgenius`` provides a simple interface to the song, artist, and
lyrics data stored on `Genius.com`_.

Using this library you can convienently access the content on Genius.com
And much more using the public API.

You can use ``pip`` to install lyricsgenius:

.. code:: bash

   pip install lyricsgenius

LyricsGenius provides lots of features to work with. For example, let's
download all the lyrics of an artist's songs, and save them to a JSON
file:

.. code:: python

   from lyricsgenius import Genius

   genius = Genius(token)
   genius.search_artist('Andy Shauf')
   artist.save_lyrics()

But before using the library you will need to get an access token. Head over
to :ref:`setup` to get started.

.. toctree::
   :maxdepth: 1
   :caption: Library

   reference
   release_notes


.. toctree::
   :maxdepth: 1
   :caption: Guide

   setup
   usage
   how_it_works
   text_formatting
   other_guides


.. toctree::
   :maxdepth: 2
   :caption: Misc

   contributing

.. _Genius.com: https://www.genius.com
.. _“Words are flowing out like endless rain into a paper cup”:
   https://genius.com/3287551
.. _“Moses wrote my name in gold and Kanye did the eulogy”:
   https://genius.com/10185147
.. _`Beautiful Soup`: https://www.crummy.com/software/BeautifulSoup/
