.. _how-it-works:
.. currentmodule:: lyricsgenius


How It Works
#############
LyricsGenius interfaces with Genius.com in two different ways:
the authenticated developer API and the unauthenticated public API.


Developer API
*************
The developer API is available through
`api.genius.com <http://api.genius.com>`_, and provides access to song, artist,
and annotation search amongst other data sources. The endpoints within the
developer API require a (free) access token. The developer API is accessed
through the :class:`API` class.


Public API
**********
The public API can be accessed without authentication and is essentially the
same service end-users access through the browser. The public API
can be called at `genius.com/api <http://genius.com/api>`_. These public API
methods are available through the :class:`PublicAPI` class.


Genius Class
************
The :ref:`genius` class is a high-level interface for the content on
Genius.com, inheriting from both the :class:`API` and :class:`PublicAPI`
classes. The :ref:`genius` class provides methods from the two API classes
mentioned above as well as useful methods like :meth:`Genius.search_song`
for accessing song lyrics and more.


Lyrics
******
Genius has legal agreements with music publishers and considers the lyrics
on their website to be a legal property of Genius, and won't allow you
to re-use their lyrics without explicit licensing. They even 
`sued Google on grounds of stolen lyrics`_, asking for $50 million in damages,
but `to no avail`_. So it shouldn't come as a surprise if they don't
provide lyrics in calls to the API. So how does LyricsGenius get the lyrics?

LyricsGenius uses a web-scraping library called `Beautiful Soup`_
to scrape lyrics from the song's page on Genius. Scraping the lyrics in
this way violates Genius' terms of service. If you intend to use the lyrics for
personal purposes, that shouldn't be cause for trouble, but other than that,
you should inquire what happens when you violate the terms this way.
As a reminder, LyricsGenius is not responsible for your usage of the library.


.. _the Genius API: http://genius.com/api-clients\
.. _create a new API client: https://genius.com/api-clients/new
.. _sued Google on grounds of stolen lyrics: https://www.theverge.com/
    2020/8/11/21363692/google-genius-lyrics-lawsuit-scraping-copyright
    -yelp-antitrust-competition
.. _to no avail: https://www.theverge.com/2020/8/11/21363692/
    google-genius-lyrics-lawsuit-scraping-copyright-yelp-antitrust-competition
.. _Beautiful Soup: https://pypi.org/project/beautifulsoup4/
