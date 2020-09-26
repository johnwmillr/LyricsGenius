.. _artist:
.. currentmodule:: lyricsgenius.artist
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Artist

Artist
=======================
The Artist object which holds the details of the artist
and the :ref:`song` objects of that artist.

Properties
-----------
.. autosummary::
   :nosignatures:

   Artist.name
   Artist.image_url
   Artist.songs


Methods
--------
.. autosummary::
   :nosignatures:

   Artist.add_song
   Artist.to_json
   Artist.to_text
   Artist.save_lyrics

.. autoclass:: lyricsgenius.artist.Artist
    :members:
    :exclude-members: get_song
    :member-order: bysource
    :no-show-inheritance:
