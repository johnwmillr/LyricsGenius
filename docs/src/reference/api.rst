.. _api:
.. currentmodule:: lyricsgenius
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: API

API
===
The :ref:`Genius` class inherits this class, and it's recommended to
call the methods using the Genius class rather than accessing this
class directly.

.. autoclass:: API
   :show-inheritance:


Account Methods
---------------
.. autosummary::
   :nosignatures:

   API.account


.. automethod:: API.account


Annotation Methods
------------------
.. autosummary::
   :nosignatures:

   API.annotation
   API.create_annotation
   API.delete_annotation
   API.downvote_annotation
   API.unvote_annotation
   API.upvote_annotation

.. automethod:: API.annotation
.. automethod:: API.create_annotation
.. automethod:: API.delete_annotation
.. automethod:: API.downvote_annotation
.. automethod:: API.unvote_annotation
.. automethod:: API.upvote_annotation


Artist Methods
--------------
.. autosummary::
   :nosignatures:

   API.artist
   API.artist_songs

.. automethod:: API.artist
.. automethod:: API.artist_songs


Referents Methods
-----------------
.. autosummary::
   :nosignatures:

   API.referents

.. automethod:: API.referents


Search Methods
-----------------
.. autosummary::
   :nosignatures:

   API.search_songs

.. automethod:: API.search_songs


Song Methods
-----------------
.. autosummary::
   :nosignatures:

   API.song

.. automethod:: API.song


Web Page Methods
-----------------
.. autosummary::
   :nosignatures:

   API.web_page

.. automethod:: API.web_page


Public API
==========
The :ref:`Genius` class inherits this class, and it's recommended to
call the methods using the Genius class rather than accessing this
class directly.

.. autoclass:: PublicAPI
   :members:
   :member-order: bysource
   :no-show-inheritance: 


Album Methods
-------------
.. autosummary::
   :nosignatures:

   PublicAPI.album
   PublicAPI.albums_charts
   PublicAPI.album_comments
   PublicAPI.album_cover_arts
   PublicAPI.album_leaderboard
   PublicAPI.album_tracks


.. automethod:: PublicAPI.album
.. automethod:: PublicAPI.albums_charts
.. automethod:: PublicAPI.album_comments
.. automethod:: PublicAPI.album_cover_arts
.. automethod:: PublicAPI.album_leaderboard
.. automethod:: PublicAPI.album_tracks


Annotation Methods
------------------
.. autosummary::
   :nosignatures:

   PublicAPI.annotation
   PublicAPI.annotation_edits
   PublicAPI.annotation_comments

.. automethod:: PublicAPI.annotation
.. automethod:: PublicAPI.annotation_edits
.. automethod:: PublicAPI.annotation_comments


Article Methods
---------------
.. autosummary::
   :nosignatures:

   PublicAPI.article
   PublicAPI.article_comments
   PublicAPI.latest_articles

.. automethod:: PublicAPI.article
.. automethod:: PublicAPI.article_comments
.. automethod:: PublicAPI.latest_articles


Artist Methods
--------------
.. autosummary::
   :nosignatures:

   PublicAPI.artist
   PublicAPI.artist_activity
   PublicAPI.artist_albums
   PublicAPI.artist_contribution_opportunities
   PublicAPI.artist_followers
   PublicAPI.artist_leaderboard
   PublicAPI.artist_songs
   PublicAPI.search_artist_songs

.. automethod:: PublicAPI.artist
.. automethod:: PublicAPI.artist_activity
.. automethod:: PublicAPI.artist_albums
.. automethod:: PublicAPI.artist_contribution_opportunities
.. automethod:: PublicAPI.artist_followers
.. automethod:: PublicAPI.artist_leaderboard
.. automethod:: PublicAPI.artist_songs
.. automethod:: PublicAPI.search_artist_songs

Cover Art Methods
-----------------
.. autosummary::
   :nosignatures:

   PublicAPI.cover_arts

.. automethod:: PublicAPI.cover_arts


Discussion Methods
------------------
.. autosummary::
   :nosignatures:

   PublicAPI.discussion
   PublicAPI.discussions
   PublicAPI.discussion_replies

.. automethod:: PublicAPI.discussion
.. automethod:: PublicAPI.discussions
.. automethod:: PublicAPI.discussion_replies


Leaderboard Methods
-------------------
.. autosummary::
   :nosignatures:

   PublicAPI.leaderboard
   PublicAPI.charts

.. automethod:: PublicAPI.leaderboard
.. automethod:: PublicAPI.charts


Question & Answer Methods
-------------------------
.. autosummary::
   :nosignatures:

   PublicAPI.questions

.. automethod:: PublicAPI.questions


Referent Methods
----------------
.. autosummary::
   :nosignatures:

   PublicAPI.referent
   PublicAPI.referents
   PublicAPI.referents_charts

.. automethod:: PublicAPI.referent
.. automethod:: PublicAPI.referents
.. automethod:: PublicAPI.referents_charts


Search Methods
--------------
.. autosummary::
   :nosignatures:

   PublicAPI.search
   PublicAPI.search_all
   PublicAPI.search_albums
   PublicAPI.search_artists
   PublicAPI.search_lyrics
   PublicAPI.search_songs
   PublicAPI.search_users
   PublicAPI.search_videos

.. automethod:: PublicAPI.search
.. automethod:: PublicAPI.search_all
.. automethod:: PublicAPI.search_albums
.. automethod:: PublicAPI.search_artists
.. automethod:: PublicAPI.search_lyrics
.. automethod:: PublicAPI.search_songs
.. automethod:: PublicAPI.search_users
.. automethod:: PublicAPI.search_videos


Song Methods
------------
.. autosummary::
   :nosignatures:

   PublicAPI.song_activity
   PublicAPI.song_comments
   PublicAPI.song_contributors

.. automethod:: PublicAPI.song
.. automethod:: PublicAPI.song_activity
.. automethod:: PublicAPI.song_comments
.. automethod:: PublicAPI.song_contributors


User Methods
------------
.. autosummary::
   :nosignatures:

   PublicAPI.user
   PublicAPI.user_accomplishments
   PublicAPI.user_following
   PublicAPI.user_followers
   PublicAPI.user_contributions
   PublicAPI.user_annotations
   PublicAPI.user_articles
   PublicAPI.user_pyongs
   PublicAPI.user_questions_and_answers
   PublicAPI.user_suggestions
   PublicAPI.user_transcriptions
   PublicAPI.user_unreviewed

.. automethod:: PublicAPI.user
.. automethod:: PublicAPI.user_accomplishments
.. automethod:: PublicAPI.user_following
.. automethod:: PublicAPI.user_followers
.. automethod:: PublicAPI.user_contributions
.. automethod:: PublicAPI.user_annotations
.. automethod:: PublicAPI.user_articles
.. automethod:: PublicAPI.user_pyongs
.. automethod:: PublicAPI.user_questions_and_answers
.. automethod:: PublicAPI.user_suggestions
.. automethod:: PublicAPI.user_transcriptions
.. automethod:: PublicAPI.user_unreviewed


Video Methods
-------------
.. autosummary::
   :nosignatures:

   PublicAPI.video
   PublicAPI.videos

.. automethod:: PublicAPI.video
.. automethod:: PublicAPI.videos


Misc. Methods
-------------
Miscellaneous methods that are mostly standalones.

.. autosummary::
   :nosignatures:

   PublicAPI.line_item
   PublicAPI.voters

.. automethod:: PublicAPI.line_item
.. automethod:: PublicAPI.voters
