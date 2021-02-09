.. _release-notes:
.. currentmodule:: lyricsgenius

Release notes
=============
3.0.0 (2021-02-08)
------------------
New
***

-  All requests now go through the ``Sender`` object. This provides
   features such as retries ``genius.retries`` and handling HTTP and
   timeout errors. For more info have a look at the guide about `request
   error handling`_.
-  Added ``OAuth2`` class to help with OAuth2 authentication.
-  Added ``PublicAPI`` class to allow accessing methods of the public
   API (genius.com/api). Check `this page`_ for a list of available
   methods.
-  Added the ``Album`` type and the ``genius.search_album()`` method.
-  Added the ``genius.tag()`` method to get songs by tag.
-  All API endpoints are now supported (e.g. ``upvote_annotation``).
-  New additions to the docs.

Changed
*******

-  ``GENIUS_CLIENT_ACCESS_TOKEN`` env var has been renamed to
   ``GENIUS_ACCESS_TOKEN``.
-  ``genius.client_access_token`` has been renamed to
   ``genius.access_token``.
-  ``genius.search_song()`` will also accept ``song_id``.
-  Lyrics won't be fetched for instrumental songs and their lyrics will
   be set to ``""``. You can check to see if a song is instrumental
   using ``Song.instrumental``.
-  Renamed all interface methods to remove redundant ``get_``
   (``genius.get_song`` is now ``genius.song``).
-  Renamed the lyrics method to ``genius.lyrics()`` to allow use by
   users. It accepts song URLs and song IDs.
-  Reformatted the types. Some attributes won't be available anymore.
   More info on the `types page`_.
-  ``save_lyrics()`` will save songs with ``utf8`` encoding when
   ``extension='txt'``.
-  Using ``Genius()`` will check for the env var
   ``GENIUS_ACCESS_TOKEN``.

Other (CI, etc)
***************

-  Bumped ``Sphinx`` to 3.3.0

.. _request error handling: https://lyricsgenius.readthedocs.io/en/master/other_guides.html#request-errors
.. _this page: https://lyricsgenius.readthedocs.io/en/latest/reference/genius.html
.. _types page: https://lyricsgenius.readthedocs.io/en/latest/reference/types.html#types


2.0.2 (2020-09-26)
------------------
Added
*****
-  Added optional ``ensure_ascii`` parameter to the
   following methods:
   :meth:`Genius.save_artists <api.Genius.save_artists>`,
   :meth:`Song.save_lyrics <types.Song.save_lyrics>`,
   :meth:`Song.to_json <types.Song.to_json>`,
   :meth:`Artist.save_lyrics <types.Artist.save_lyrics>`
   and :meth:`Artist.to_json <types.Artist.to_json>`


2.0.1 (2020-09-20)
------------------
Changed
*******
- :func:`Genius.lyrics`- Switched to using
  regular expressions to find the ``new_div`` (:issue:`154`).
