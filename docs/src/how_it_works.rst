.. _how-it-works:
.. currentmodule:: lyricsgenius


How It Works
#############
LyricsGenius makes two kinds of calls to the Genius API. The first one is
the API that requires an access token, and the other one to the public API.


API
**********
This API is available through
`api.genius.com <http://api.genius.com>`_, and provides access to features like
searching songs, getting song or annotation data by
providing their ID, and some other features. But the problem with this API
is that Genius has only exposed a little of the whole API. These methods are
available throught the :class:`API` class.
This is not the case for the second kind of calls: the ones to the public API.


Public API
***************
The public API is the API that doesn't require an access token and can be
accessed by anyone (end-users use this on their browsers). The public API
can be called at `genius.com/api <http://genius.com/api>`_. This API
exposes a whole other set of features (and sometimes access to the same) than
the *token API*. These methods are available throught the
:class:`PublicAPI` class.

Although these two calls can provide you with a lot of information,
they still don't let you anywhere near what's probably the most important
thing you may want from Genius: the lyrics.


Lyrics
**********
Genius has legal agreements with music publishers and considers the lyrics
on their website to be a legal property of Genius, and won't allow you
to re-use their lyrics without explicit licensing. They even 
`sued Google on grounds of stolen lyrics`_, asking for $50 million in damages,
but `to no avail`_. So it shouldn't come as a surprise if they don't
provide lyrics in calls to
the API. So how does LyricsGenius get the lyrics?

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
