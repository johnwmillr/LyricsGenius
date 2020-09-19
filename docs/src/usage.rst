.. _usage:

Usage
==================

Import the package and search for songs by a given artist:

.. code:: python

   import lyricsgenius
   genius = lyricsgenius.Genius("my_client_access_token_here")
   artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title")
   print(artist.songs)

Search for a single song by the same artist:

.. code:: python

   song = genius.search_song("To You", artist.name)
   print(song.lyrics)

Add the song to the :ref:`artist` object:

.. code:: python

   artist.add_song(song)

Save the artist’s songs to a JSON file:

.. code:: python

   artist.save_lyrics()

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

   export GENIUS_CLIENT_ACCESS_TOKEN="my_client_access_token_here"
   python3 -m lyricsgenius --help

Search for and save lyrics to a given song:

.. code:: bash

   python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save

Search for five songs by ‘The Beatles’ and save the lyrics:

.. code:: bash

   python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save


There also examples under the docs of some methods.


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Index

   examples/snippets
   examples/example projects
