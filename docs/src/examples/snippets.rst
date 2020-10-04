.. _snippets:
.. currentmodule:: lyricsgenius

Snippets
==================
Here are some snippets showcasing how the library can be used.

- `Getting artist using API, PublicAPI and Genius`_
- `All the songs of an artist`_
- `Artist's least popular song`_
- `YouTube URL of artist's songs`_
- `Searching for a song by lyrics`_
- `Authenticating using OAuth2`_

Getting artist using API, PublicAPI and Genius
-------------------------------------------------
The following snippet will be the same for all
methods that are available in :class:`API` and :class:`PublicAPI`
(or methods that have a ``public_api`` parameter
if you're using :class:`Genius`).

.. code:: python

    from lyricsgenius import API, PublicAPI, Genius

    api = API(token)
    public = PublicAPI()
    genius = Genius(token)

    # API
    api.artist(1665)

    # PublicAPI
    public.artist(1665)

    # Genius
    # can get it using both API and PublicAPI
    genius.artist(1665)
    genius.artist(1665, public_api=True)

Note that if you use :class:`Genius` without a token, you won't be able
to use the developers API. So you'll either have to set ``public_api=True`` if
the method supports it, or set ``Genius.public_api`` to ``True`` to have
all the calls that support it be made using the public API.

.. code:: python

    genius = Genius(public_api=True)

    # the following calls will be equivalent
    genius.artist(1665)
    genius.artist(1665, public_api=True)



All the songs of an artist
--------------------------

.. code:: python

    from lyricsgenius import Genius

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
                                          # public_api=Tru
                                          )
        # public_api=True will make the call using the public API 
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
    
    from lyricsgenius import Genius

    genius = Genius(token)

    request = genius.search_lyrics('Jeremy can we talk a minute?')
    for hit in request['sections'][0]['hits']:
        print(hit['result']['title'])

Using :meth:`search_all <Genius.search_all>`:

.. code:: python
    
    from lyricsgenius import Genius

    genius = Genius(token)

    request = genius.search_all('Jeremy can we talk a minute?')
    for hit in request['sections'][2]['hits']:
        print(hit['result']['title'])


Authenticating using OAuth2
---------------------------
Authenticating yourself
^^^^^^^^^^^^^^^^^^^^^^^
Whitelist a redirect URI in your app's page on Genius. Any redirect
URI will work (for example ``http://example.com/callback``)

.. code:: python

    from lyricsgenius import OAuth2, Genius
    auth = OAuth2('my_client_id',
                  'my_redirect_uri',
                  scope='all',
                  client_only_app=True)
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
                  scope='all')

    # this part is the same
    url_for_user = auth.url
    print('Redirecting you to ' + url_for_user)
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
