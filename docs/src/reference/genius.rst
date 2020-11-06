.. _genius:
.. currentmodule:: lyricsgenius
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Genius


Genius
=======================
The Genius class provides a high-level interface to the Genius API. This
class provides convenient access to the standard API (:class:`API`), the
public API (:class:`PublicAPI`), and additional features such as
downloading lyrics.

.. autoclass:: Genius
   :show-inheritance:


Account Methods
---------------
.. autosummary::
   :nosignatures:

   Genius.account


.. automethod:: Genius.account


Album Methods
-------------
.. autosummary::
   :nosignatures:

   Genius.album
   Genius.albums_charts
   Genius.album_comments
   Genius.album_cover_arts
   Genius.album_leaderboard
   Genius.album_tracks


.. automethod:: Genius.album
.. automethod:: Genius.albums_charts
.. automethod:: Genius.album_comments
.. automethod:: Genius.album_cover_arts
.. automethod:: Genius.album_leaderboard
.. automethod:: Genius.album_tracks


Annotation Methods
------------------
.. autosummary::
   :nosignatures:

   Genius.annotation
   Genius.annotation_edits
   Genius.annotation_comments
   Genius.create_annotation
   Genius.delete_annotation
   Genius.downvote_annotation
   Genius.unvote_annotation
   Genius.upvote_annotation

.. automethod:: Genius.annotation
.. automethod:: Genius.annotation_edits
.. automethod:: Genius.annotation_comments
.. automethod:: Genius.create_annotation
.. automethod:: Genius.delete_annotation
.. automethod:: Genius.downvote_annotation
.. automethod:: Genius.unvote_annotation
.. automethod:: Genius.upvote_annotation


Article Methods
---------------
.. autosummary::
   :nosignatures:

   Genius.article
   Genius.article_comments
   Genius.latest_articles

.. automethod:: Genius.article
.. automethod:: Genius.article_comments
.. automethod:: Genius.latest_articles


Artist Methods
--------------
.. autosummary::
   :nosignatures:

   Genius.artist
   Genius.artist_activity
   Genius.artist_albums
   Genius.artist_contribution_opportunities
   Genius.artist_followers
   Genius.artist_leaderboard
   Genius.artist_songs
   Genius.save_artists
   Genius.search_artist_songs


.. automethod:: Genius.artist
.. automethod:: Genius.artist_activity
.. automethod:: Genius.artist_albums
.. automethod:: Genius.artist_contribution_opportunities
.. automethod:: Genius.artist_followers
.. automethod:: Genius.artist_leaderboard
.. automethod:: Genius.artist_songs
.. automethod:: Genius.save_artists
.. automethod:: Genius.search_artist_songs


Cover Art Methods
-----------------
.. autosummary::
   :nosignatures:

   Genius.cover_arts

.. automethod:: Genius.cover_arts


Discussion Methods
------------------
.. autosummary::
   :nosignatures:

   Genius.discussion
   Genius.discussions
   Genius.discussion_replies

.. automethod:: Genius.discussion
.. automethod:: Genius.discussions
.. automethod:: Genius.discussion_replies


Leaderboard Methods
-------------------
.. autosummary::
   :nosignatures:

   Genius.leaderboard
   Genius.charts

.. automethod:: Genius.leaderboard
.. automethod:: Genius.charts


Question & Answer Methods
-------------------------
.. autosummary::
   :nosignatures:

   Genius.questions

.. automethod:: Genius.questions


Referent Methods
----------------
.. autosummary::
   :nosignatures:

   Genius.referent
   Genius.referents
   Genius.referents_charts

.. automethod:: Genius.referent
.. automethod:: Genius.referents
.. automethod:: Genius.referents_charts


Search Methods
--------------
.. autosummary::
   :nosignatures:

   Genius.search
   Genius.search_all
   Genius.search_albums
   Genius.search_artist
   Genius.search_artists
   Genius.search_lyrics
   Genius.search_song
   Genius.search_songs
   Genius.search_users
   Genius.search_videos

.. automethod:: Genius.search
.. automethod:: Genius.search_all
.. automethod:: Genius.search_albums
.. automethod:: Genius.search_artist
.. automethod:: Genius.search_artists
.. automethod:: Genius.search_lyrics
.. automethod:: Genius.search_song
.. automethod:: Genius.search_songs
.. automethod:: Genius.search_users
.. automethod:: Genius.search_videos


Song Methods
------------
.. autosummary::
   :nosignatures:

   Genius.song
   Genius.song_activity
   Genius.song_annotations
   Genius.song_comments
   Genius.song_contributors
   Genius.lyrics

.. automethod:: Genius.song
.. automethod:: Genius.song_activity
.. automethod:: Genius.song_annotations
.. automethod:: Genius.song_comments
.. automethod:: Genius.song_contributors
.. automethod:: Genius.lyrics


User Methods
------------
.. autosummary::
   :nosignatures:

   Genius.user
   Genius.user_accomplishments
   Genius.user_following
   Genius.user_followers
   Genius.user_contributions
   Genius.user_annotations
   Genius.user_articles
   Genius.user_pyongs
   Genius.user_questions_and_answers
   Genius.user_suggestions
   Genius.user_transcriptions
   Genius.user_unreviewed

.. automethod:: Genius.user
.. automethod:: Genius.user_accomplishments
.. automethod:: Genius.user_following
.. automethod:: Genius.user_followers
.. automethod:: Genius.user_contributions
.. automethod:: Genius.user_annotations
.. automethod:: Genius.user_articles
.. automethod:: Genius.user_pyongs
.. automethod:: Genius.user_questions_and_answers
.. automethod:: Genius.user_suggestions
.. automethod:: Genius.user_transcriptions
.. automethod:: Genius.user_unreviewed


Video Methods
-------------
.. autosummary::
   :nosignatures:

   Genius.video
   Genius.videos

.. automethod:: Genius.video
.. automethod:: Genius.videos


Web Page Methods
-----------------
.. autosummary::
   :nosignatures:

   Genius.web_page

.. automethod:: Genius.web_page


Misc. Methods
-------------
Miscellaneous methods that are mostly standalones.

.. autosummary::
   :nosignatures:

   Genius.tag
   Genius.line_item
   Genius.voters

.. automethod:: Genius.tag
.. automethod:: Genius.line_item
.. automethod:: Genius.voters
