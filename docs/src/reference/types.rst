.. _types:
.. currentmodule:: lyricsgenius.types

Types
=====
Package-defined types.

Currently, the types defined here are only returned by
:meth:`Genius.search_artist` and :meth:`Genius.search_song`.


Artist
------
The Artist object which holds the details of the artist
and the `Song`_ objects of that artist.


Properties
^^^^^^^^^^^
.. autosummary::
   :nosignatures:

   Artist.name
   Artist.image_url
   Artist.songs


Methods
^^^^^^^^
.. autosummary::
   :nosignatures:

   Artist.song
   Artist.add_song
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


Properties
^^^^^^^^^^^
.. autosummary::
   :nosignatures:

   Song.title
   Song.artist
   Song.lyrics
   Song.album
   Song.year
   Song.url
   Song.album_url
   Song.featured_artists
   Song.producer_artists
   Song.media
   Song.writer_artists
   Song.song_art_image_url


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

