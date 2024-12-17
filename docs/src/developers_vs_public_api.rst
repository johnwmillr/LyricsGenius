.. _developers-vs-public-api:
.. currentmodule:: lyricsgenius

Developers vs. Public API
#########################
It's important to know of the limitations and the risks that come with
Genius's APIs. Please read the sections below one by one to get a view
of the Developers and the Public API.


Developers API
==============

This is the official Genius API. Although limited in functionality, this
API is supported by Genius and will not change without further notice.
You will need a (free) access token to use this API. Methods of this API
are available in the :class:`API` class.

Public API
==========

This API is the one used by your browser when you visit Genius. It
offers far more functionalities, but is not officially supported by
Genius and is subject to change without any notice. You may also get
banned or limited if you send too many requests to the endpoints of this
API; usually, you would notice this by getting HTTP 403 errors.
Furthermore, due to Genius's CaptCha, some IPs may experience HTTP 403
errors when using this API. Methods of this API are available in the
:class:`PublicAPI` class.

Genius.allow_public_api
=======================

We've added this attribute to the :class:`Genius` class to make sure that the
users know what methods they are using and what risks are involved. For
example when using the method convenience method
:meth:`Genius.search_song`, a search is carried out using the Public API
methods, and then the song data is fetched from the Developers API. For
another example, we can point to :meth:`Genius.album`. Genius doesn't
have an official API for getting album data, but it can be done using
the Public API (the :class:`Genius` inherits the :class:`API` and
:class:`PublicAPI` and gets all of their methods to provide convenient
access). If you believe that you can accept the risks that come with the
Public API, feel free to use the Public API.
