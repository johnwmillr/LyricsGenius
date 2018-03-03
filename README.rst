Scraping song lyrics from Genius.com
====================================

|Build Status| |PyPI version| |Python version|

Setup
-----

This repository is intended to provide an easy interface for
programatically accessing the song information stored on
`Genius.com <https://www.genius.com>`__. Check out `my blog
post <http://www.johnwmillr.com/scraping-genius-lyrics/>`__ for a more
thorough description of the package and its usage.

To use the Genius API you’ll need to sign up for a (free) client that
authorizes you to `access their API <http://genius.com/api-clients>`__.
You’ll need to supply your ``client_access_token`` from Genius when
using this module. See
`Usage <https://github.com/johnwmillr/LyricsGenius#usage>`__ below for
an example.

Installation
------------

*LyricsGenius* requires Python 3.

The easiest way to use this package is to install it via
`PyPI <https://pypi.python.org/pypi/lyricsgenius>`__ using ``pip``:

``$pip install lyricsgenius``

| If you’d prefer to clone the repository and install it yourself,
  follow these steps: 1. Clone this repo:
| ``$git clone https://github.com/johnwmillr/LyricsGenius.git`` 2. Enter
  the directory created:
| ``$cd LyricsGenius`` 3. Install using pip:
| ``$pip install .``

Usage
-----

.. code:: python

    >>> import lyricsgenius as genius
    >>> api = genius.Genius('my_client_access_token_here')
    >>> artist = api.search_artist('Andy Shauf', max_songs=3)
    Searching for Andy Shauf...

    Song 1: "Alexander All Alone"
    Song 2: "Begin Again"
    Song 3: "Comfortable With Silence"

    Reached user-specified song limit (3).
    Found 3 songs.

    Done.
    >>> print(artist)
    Andy Shauf, 3 songs
    >>> song = api.search_song('To You',artist.name)
    Searching for "To You" by Andy Shauf...
    Done.
    >>> print(song)
    "To You" by Andy Shauf:
        Jeremy can we talk a minute
        I've got some things that I need to
        Get off of my chestI know that we h...
    >>> artist.add_song(song)
    >>> print(artist)
    Andy Shauf, 4 songs

You can also call the package from the command line. When ran from the
command line, the package expects to find an environment variable with
your Genius client access token.

::

    $export GENIUS_CLIENT_ACCESS_TOKEN="my_client_access_token_here"
    $python3 -m lyricsgenius --search-song 'Begin Again' 'Andy Shauf'
    $python3 -m lyricsgenius --search-artist 'Lupe Fiasco' 3

Example projects
----------------

-  `Textual analysis of popular country
   music <http://www.johnwmillr.com/trucks-and-beer/>`__

I’d love to have more examples to list here! Let me know if you’ve made
use of this wrapper for one of your own projects, and I’ll list it here.

Contributing
------------

Please contribute! I’d love to have collaborators on this project. If
you want to add features, suggest improvements, or have other comments,
just make a pull request or raise an issue.

.. |Build Status| image:: https://travis-ci.org/johnwmillr/LyricsGenius.svg?branch=master
   :target: https://travis-ci.org/johnwmillr/LyricsGenius
.. |PyPI version| image:: https://badge.fury.io/py/lyricsgenius.svg
   :target: https://pypi.python.org/pypi/lyricsgenius
.. |Python version| image:: https://img.shields.io/badge/python-3.x-brightgreen.svg
   :target: https://pypi.python.org/pypi/lyricsgenius
