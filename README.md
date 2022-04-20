# AGenius.py
`AGenius.py` is a [LyricsGenius](https://github.com/johnwmillr/LyricsGenius) fork, making it easy to use, and async ready.

## Key Features
* Pythonic `async`/`await`.
* Removed every possible instance of the `Public API` to make it **safer**.

## Setup
You'll need a free [Genius](https://genius.com) account to get access to 
the [Genius API](https://genius.com/api-clients). This provides an `access_token` that is required.

## Installation
**Python 3.9 or higher**
You can use pip:
```shell
# Linux
python3 -m pip install agenius

# Windows
py -3 -m pip install agenius
```

## Examples
Importing the package and initiating the main class:
```python
import agenius
genius = agenius.Genius(token)
```
`PUBLIC_API` has been removed in this version. You have to pass an access token to the `Genius()` class.

To search for a specific song, you can either search by the `title` or `song_id`:
```python
# by title
song = await genius.search_song("Never Gonna Give You Up", "Rick Astley")

# by song_id
song = await genius.search_song(song_id=84851)
```

You can also look up artists and their songs via `artist_id`'s:
```python
# look up an artist
artist = await genius.artist(artist_id=artist_id)

# look up their songs
song_list = await genius.artist_songs(artist_id=artist_id, per_page=10, sort="title")
```

Configurable parameters in the `Genius()` class:
```python
genius.verbose = False  # Turns status messages off
genius.excluded_terms = ["(Remix)", "(Live)"]  # Exclude songs with these words in their title
```

## Big Examples
### Get a song's lyrics

```python
import agenius

genius = agenius.Genius(token)

song = await genius.search_song("Never Gonna Give You Up")
lyrics = song.lyrics
```
### Get a list of an artist's songs, and get the lyrics of every one of them

```python
import agenius
genius = agenius.Genius(token)

async def get_lyrics(artist_id):
    song_list = await genius.artist_songs(artist_id, per_page=50, sort="title")

    lyrics = {}
    async for song in song_list:
        lyrics[song["title"]] = song.lyrics
    return lyrics
```
