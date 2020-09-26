.. _release-notes:
.. currentmodule:: lyricsgenius

Release notes
=============
2.0.2 (2020-??-??)
------------------
Added
*****
-  Added optional ``ensure_ascii`` parameter to the
   following methods:
   :meth:`Genius.save_artists <api.Genius.save_artists>`,
   :meth:`Song.save_lyrics <song.Song.save_lyrics>`,
   :meth:`Song.to_json <song.Song.to_json>`,
   :meth:`Artist.save_lyrics <artist.Artist.save_lyrics>`
   and :meth:`Artist.to_json <artist.Artist.save_lyrics>`


2.0.1 (2020-09-20)
------------------
Changed
*******
- :func:`Genius._scrape_song_lyrics_from_url`- Switched to using
   regular expressions to find the ``new_div`` (:issue:`154`).

