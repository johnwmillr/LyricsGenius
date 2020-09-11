.. _snippets:

Snippets
==================
Here are some snippets showcasing how the library can be used.


- `All the songs of an artist`_
- `Artist's least popular song`_
- `YouTube URL of artist's songs`_
- `Searching for a song by lyrics`_
- `Authenticating using OAuth2`_

All the songs of an artist
------------------------------

.. code:: python

    from lyricsgenius import Genius

    genius = Genius(token)
    genius.search_artist('Andy Shauf')
    artist.save_lyrics()


Artist's least popular song
----------------------------
.. code:: python

    genius = Genius(token)

    artist = genius.search_artist('Andy Shauf', max_songs=1)
    page = 1
    songs = []
    while page:
        request = genius.get_artist_songs(artist._id,
                                          sort='popularity',
                                          per_page=50,
                                          page=page)
        songs.extend(request['songs'])
        page = request['next_page']
    least_popular_song = genius.search_song(songs[-1]['title'], artist.name)
    print(least_popular_song.lyrics)


YouTube URL of artist's songs
------------------------------
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
-------------------------------
.. code:: python
    
    from lyricsgenius import Genius

    genius = Genius(token)

    request = genius.search_genius_web('Jeremy can we talk a minute?')
    for hit in request['sections'][2]['hits']:
        print(hit['result']['title'])


Authenticating using OAuth2
---------------------------
Authenticating yourself
^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    from lyricsgenius import OAuth2, Genius
    auth = OAuth2('my_client_id',
                  'my_redirect_uri',
                  scope='all',
                  client_only_app=True)  # if we don't set this,
                  we'll also have to provide client_secret
    token = auth.prompt_user()

    genius = Genius(token)

Authenticating another user
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    from lyricsgenius import OAuth2, Genius

    # client-only app
    auth = OAuth2('my_client_id',
                  'my_redirect_uri',
                  scope='all',
                  client_only_app=True)

    # full code exhange app
    auth = OAuth2('my_client_id',
                  'my_redirect_uri',
                  'my_client_secret',
                  scope='all',
                  client_only_app=True)

    # this part is the same
    url_for_user = auth.url
    print('Redirecting you to {}'.format(url_for_user))
    redirected_url = 'https://example.com/?code=some_code'
    token = auth.get_user_token(redirected_url)

    genius = Genius(token)

.. Note:: 
    The only difference the process of getting the user token
    using a client-only application or the full code exchange
    is in the parameters you pass to the OAuth2 object.
    In the example above we're using a client-only app
    that doesn't need the client secret and we also have to
    set :obj:`client_only_app` to *True*.
    If you intend to use the full code exchange which is safer,
    set :obj:`client_secret` when instantiating the OAUTH2 object
    and set :obj:`client_only_app` to *False* (it's *False* by
    default).

.. Note::
    Visit the `Authentication section`_ in the Genius API documentation
    to find out more about client-only apps and the full code exchange
    process.


.. _`Authentication section`: https://docs.genius.com/#/authentication-h1
