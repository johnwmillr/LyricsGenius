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
   Track

.. autoclass:: Stats
    :members:
    :member-order: bysource
    :no-show-inheritance:

.. autoclass:: Track
    :members:
    :member-order: bysource
    :no-show-inheritance:


Album
------
An album from Genius that has the album's songs and their lyrics.

Attributes
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Attribute
     - Type

   * - _type
     - :obj:`str`

   * - api_path
     - :obj:`str`

   * - artist
     - :class:`Artist`

   * - cover_art_thumbnail_url
     - :obj:`str`

   * - cover_art_url
     - :obj:`str`

   * - full_title
     - :obj:`str`

   * - id
     - :obj:`int`

   * - name
     - :obj:`str`

   * - name_with_artist
     - :obj:`str`

   * - release_date_components
     - :class:`datetime`

   * - tracks
     - :obj:`list` of :class:`Track`

   * - url
     - :obj:`str`


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

Attributes
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Attribute
     - Type


   * - api_path
     - :obj:`str`

   * - header_image_url
     - :obj:`str`

   * - id
     - :obj:`int`

   * - image_url
     - :obj:`str`

   * - is_meme_verified
     - :obj:`bool`

   * - is_verified
     - :obj:`bool`

   * - name
     - :obj:`str`

   * - songs
     - :obj:`list`

   * - url
     - :obj:`str`

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

Attributes
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Attribute
     - Type


   * - annotation_count
     - :obj:`int`

   * - api_path
     - :obj:`str`

   * - artist
     - :obj:`str`

   * - full_title
     - :obj:`str`

   * - header_image_thumbnail_url
     - :obj:`str`

   * - header_image_url
     - :obj:`str`

   * - id
     - :obj:`int`

   * - lyrics
     - :obj:`str`

   * - lyrics_owner_id
     - :obj:`int`

   * - lyrics_state
     - :obj:`str`

   * - path
     - :obj:`str`

   * - primary_artist
     - :class:`Artist`

   * - pyongs_count
     - :obj:`int`

   * - song_art_image_thumbnail_url
     - :obj:`str`

   * - song_art_image_url
     - :obj:`str`

   * - stats
     - :class:`Stats`

   * - title
     - :obj:`str`

   * - title_with_featured
     - :obj:`str`

   * - url
     - :obj:`str`

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

