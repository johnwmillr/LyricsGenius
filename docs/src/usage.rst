.. _usage:
.. currentmodule:: lyricsgenius

Usage
==================

Import the package and search for songs by a given artist:

.. code:: python

   from lyricsgenius import Genius

   genius = Genius(token)
   artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title")
   print(artist.songs)

Search for a single song by the same artist:

.. code:: python

   # Way 1
   song = genius.search_song("To You", artist.name)

   # Way 2
   # this will search artist.songs first
   # and if not found, uses search_song
   song = artist.song("To You")

   print(song.lyrics)

Add the song to the :class:`Artist <types.Artist>` object:

.. code:: python

   artist.add_song(song)
   # add_song accepts song names as well:
   # artist.add_song("To You")

Save the artist’s songs to a JSON file:

.. code:: python

   artist.save_lyrics()

Searching for an album and saving it:

.. code:: python

   album = genius.search_album("The Party", "Andy Shauf")
   album.save_lyrics()

There are various options configurable as parameters within the
:ref:`genius` class:

.. code:: python

   # Turn off status messages
   genius.verbose = False 

   # Remove section headers (e.g. [Chorus]) from lyrics when searching
   genius.remove_section_headers = True 

   # Include hits thought to be non-songs (e.g. track lists)
   genius.skip_non_songs = False

   # Exclude songs with these words in their title
   genius.excluded_terms = ["(Remix)", "(Live)"]

You can also call the package from the command line:

.. code:: bash

   export GENIUS_ACCESS_TOKEN="my_access_token_here"
   python3 -m lyricsgenius --help

Search for and save lyrics to a given song and album:

.. code:: bash

   python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save
   python3 -m lyricsgenius album "The Party" "Andy Shauf" --save

Search for five songs by ‘The Beatles’ and save the lyrics:

.. code:: bash

   python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save


You might also like checking out the :ref:`snippets` page. 


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Index

   examples/snippets
   examples/example projects
