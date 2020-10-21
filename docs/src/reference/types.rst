.. _types:
.. currentmodule:: lyricsgenius.types

Types
=====
Package-defined types.

Currently, the types defined here are only returned by
:meth:`Genius.search_album`, :meth:`Genius.search_artist`
and :meth:`Genius.search_song`.


All of the attributes listed in the types are guaranteed to be present
in the returned object. To access other values that are
in the response body, use :meth:`to_dict`.

Base
----
Base classes.


Classes
^^^^^^^
.. autosummary::
   :nosignatures:

   Stats

.. autoclass:: Stats
    :members:
    :member-order: bysource
    :no-show-inheritance:


Album
------
An album from Genius that has the album's songs and their lyrics.


Methods
^^^^^^^^
.. autosummary::
   :nosignatures:

   Album.to_dict
   Album.to_json
   Album.to_text
   Album.save_lyrics


.. autoclass:: Album
    :members:
    :member-order: bysource
    :no-show-inheritance:


Artist
------
The Artist object which holds the details of the artist
and the `Song`_ objects of that artist.


Methods
^^^^^^^^
.. autosummary::
   :nosignatures:

   Artist.song
   Artist.add_song
   Artist.to_dict
   Artist.to_json
   Artist.to_text
   Artist.save_lyrics


.. autoclass:: Artist
    :members:
    :member-order: bysource
    :no-show-inheritance:


Song
----
This is the Song object which holds the details of the song.

Methods
^^^^^^^^
.. autosummary::
   :nosignatures:

   Song.to_dict
   Song.to_json
   Song.to_text
   Song.save_lyrics


.. autoclass:: Song
    :members:
    :member-order: bysource
    :no-show-inheritance:

