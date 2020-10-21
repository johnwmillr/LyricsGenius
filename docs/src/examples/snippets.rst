.. _snippets:
.. currentmodule:: lyricsgenius

Snippets
==================
Here are some snippets showcasing how the library can be used.

- `Getting song lyrics by URL or ID`_
- `All the songs of an artist`_
- `Artist's least popular song`_
- `YouTube URL of artist's songs`_
- `Searching for a song by lyrics`_
- `Getting the lyrics for all songs of a search`_
- `Authenticating using OAuth2`_


Getting song lyrics by URL or ID
--------------------------------
.. code:: python

    genius = Genius(token)

    # Using Song URL
    url = "https://genius.com/Andy-shauf-begin-again-lyrics"
    genius.lyrics(url)

    # Using Song ID
    # Requires an extra request to get song URL
    id = 2885745
    genius.lyrics(id)

All the songs of an artist
--------------------------

.. code:: python

    genius = Genius(token)
    genius.search_artist('Andy Shauf')
    artist.save_lyrics()


Artist's least popular song
---------------------------
.. code:: python

    genius = Genius(token)

    artist = genius.search_artist('Andy Shauf', max_songs=1)
    page = 1
    songs = []
    while page:
        request = genius.artist_songs(artist._id,
                                      sort='popularity',
                                      per_page=50,
                                      page=page,
                                      )
        songs.extend(request['songs'])
        page = request['next_page']
    least_popular_song = genius.search_song(songs[-1]['title'], artist.name)
    print(least_popular_song.lyrics)


YouTube URL of artist's songs
-----------------------------
.. code:: python

    import json
    # we have saved the songs with artist.save_lyrics() before this
    with open('saved_file.json') as f:
        data = json.load(f)
    for song in data['songs']:
        links = song['media']
        if links:
            for media in links:
                if media['provider'] == 'youtube':
                    print(print(['song'] + ': ' + media['url'])
                    break


Searching for a song by lyrics
------------------------------
Using :meth:`search_lyrics
<Genius.search_lyrics>`:

.. code:: python

    genius = Genius(token)

    request = genius.search_lyrics('Jeremy can we talk a minute?')
    for hit in request['sections'][0]['hits']:
        print(hit['result']['title'])

Using :meth:`search_all <Genius.search_all>`:

.. code:: python

    genius = Genius(token)

    request = genius.search_all('Jeremy can we talk a minute?')
    for hit in request['sections'][2]['hits']:
        print(hit['result']['title'])


Getting the lyrics for all songs of a search
--------------------------------------------
.. code:: python

    genius = Genius(token)
    lyrics = []

    songs = genius.search_songs('Begin Again Andy Shauf')
    for song in songs['hits']:
        url = song['result']['url']
        song_lyrics = genius.lyrics(url)
        # id = song['result']['id']
        # song_lyrics = genius.lyrics(id)
        lyrics.append(song_lyrics)


Authenticating using OAuth2
---------------------------
Genius provides two flows for getting a user token: the code flow
(called full code exchange) and the token flow (called client-only app).
LyricsGenius provides two class methods
:meth:`OAuth2.full_code_exchange` and :meth:`OAuth2.client_only_app` for
the aforementioned flow. Visit the `Authentication section`_ in the
Genius API documentation read more about the code and the token flow.

You'll need the client ID and the redirect URI for a client-only app.
For the full-code exchange you'll also need the client secret. The package
can get them for using these environment variables:
``GENIU_CLIENT_ID``, ``GENIUS_REDIRECT_URI``, ``GENIUS_CLIENT_SECRET``

.. code:: python

    import lyricsgenius as lg

    client_id, redirect_uri, client_secret = lg.auth_from_environment() 

Authenticating yourself
^^^^^^^^^^^^^^^^^^^^^^^
Whitelist a redirect URI in your app's page on Genius. Any redirect
URI will work (for example ``http://example.com/callback``)

.. code:: python

    from lyricsgenius import OAuth2, Genius

    # you can also use OAuth2.full_code_exchange()
    auth = OAuth2.client_only_app(
        'my_client_id',
        'my_redirect_uri',
        scope='all'
    )

    token = auth.prompt_user()

    genius = Genius(token)

Authenticating another user
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    from lyricsgenius import OAuth2, Genius

    # client-only app
    auth = OAuth2.client_only_app(
        'my_client_id',
        'my_redirect_uri',
        scope='all'
    )

    # full code exhange app
    auth = OAuth2.full_code_exchange(
        'my_client_id',
        'my_redirect_uri',
        'my_client_secret',
        scope='all'
    )

    # this part is the same
    url_for_user = auth.url
    print('Redirecting you to ' + url_for_user)
    redirected_url = 'https://example.com/?code=some_code'
    token = auth.get_user_token(redirected_url)

    genius = Genius(token)

.. _`Authentication section`: https://docs.genius.com/#/authentication-h1
