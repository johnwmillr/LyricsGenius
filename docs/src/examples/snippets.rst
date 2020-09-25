.. _snippets:
.. currentmodule:: lyricsgenius

Snippets
==================
Here are some snippets showcasing how the library can be used.

- `Getting artist using API, PublicAPI and Genius`
- `All the songs of an artist`_
- `Artist's least popular song`_
- `YouTube URL of artist's songs`_
- `Searching for a song by lyrics`_


Getting artist using API, PublicAPI and Genius
-------------------------------------------------
The following snippet will be the same for all
methods that are available in :class:`API` and :class:`PublicAPI`
(or have a ``public_api`` parameter if you're using :class:`Genius`).

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
