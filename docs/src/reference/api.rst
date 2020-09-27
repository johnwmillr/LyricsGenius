.. _api:
.. currentmodule:: lyricsgenius
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: API

API
=======================
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


Web Pages Methods
-----------------
.. autosummary::
   :nosignatures:

   API.web_page

.. automethod:: API.web_page
