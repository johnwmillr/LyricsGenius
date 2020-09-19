.. _snippets:

Snippets
==================
Here are some snippets showcasing how the library can be used.


- `All the songs of an artist`_
- `Artist's least popular song`_
- `YouTube URL of artist's songs`_
- `Searching for a song by lyrics`_


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
