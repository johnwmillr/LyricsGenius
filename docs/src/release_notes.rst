.. _release-notes:
.. currentmodule:: lyricsgenius

Release notes
=============

3.7.3
------------------

Changed
*******
-  Changed ``Genius.excluded_terms`` handling to treat default and custom
   values as case-insensitive literal substrings, fixing cases where
   parentheses or other punctuation were previously interpreted as regular
   expression tokens.
-  Reorganized test suite: extracted ``_result_is_lyrics`` tests into
   ``test_result_is_lyrics.py``, merged ``test_api.py`` into
   ``test_genius_api.py``, and converted remaining unittest-style tests
   to pytest.


3.7.1 (2025-08-17)
------------------

Changed
*******
-  Updated the unit tests to avoid making actual requests to
   the Genius API.
-  The tests now use fixtures in ``tests/fixtures/`` to mock the API
   responses.


3.7.0 (2025-05-31)
------------------
New
*******

-  Added type annotations to the codebase.
-  Uses Protocols to better define the interface of the ``PublicAPI``
   mixins.
-  Deleted the ``Stats`` class.
-  Removed the ``Track`` class, replaced its functionality with the
   ``Song`` class.
-  Swapped the order of arguments to the ``Song`` class. The ``lyrics``
   argument is now first and ``body`` is second.
-  Removed the ``Genius.save_artists()`` method because it wasn't
   helpful. You're better of just looping through a list of artists and
   calling ``Artist.save_lyrics()`` on each one.
-  Renamed the ``client_only_app`` parameter in ``OAuth2`` to
   ``app_is_client_only``.

3.6.4 (2025-05-31)
------------------
Changed
*******

-  Added a `DeprecationWarning` to the ``Song``, ``Artist``, and ``Album``
   classes. The ``Genius`` client will be removed from these classes in
   a future release.
-  Added a `DeprecationWarning` to the ``Track`` class. This class will
   be removed in a future release. Its functionality will be
   incorporated into the ``Song`` class.
-  Added a `DeprecationWarning` to the ``Stats`` class. This class will
   be removed in a future release.
-  Added a `FutureWarning` to the ``Song`` constructor. Its signature
   will change to ``Song(lyrics, body)`` instead of
   ``Song(client, json_dict, lyrics)``.

3.6.3 (2025-05-31)
------------------
Changed
*******

-  Fixed a bug where ``Genius.search_artist()`` wouldn't obey the
   ``max_songs`` parameter. Now it will return the correct number of
   songs as specified.
-  Fixed typos and removed random unicode characters.

3.0.0 (2021-02-08)
------------------
New
*****

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

-  Added optional ``ensure_ascii`` parameter to the following methods:
   :meth:`Genius.save_artists <api.Genius.save_artists>`,
   :meth:`Song.save_lyrics <types.Song.save_lyrics>`,
   :meth:`Song.to_json <types.Song.to_json>`,
   :meth:`Artist.save_lyrics <types.Artist.save_lyrics>`
   and :meth:`Artist.to_json <types.Artist.to_json>`

2.0.1 (2020-09-20)
------------------
Changed
*******

-  :func:`Genius.lyrics` - Switched to using regular expressions to find
   the ``new_div`` (:issue:`154`).
