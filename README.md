# LyricsGenius: a Python client for the Genius.com API
[![Build Status](https://travis-ci.org/johnwmillr/LyricsGenius.svg?branch=master)](https://travis-ci.org/johnwmillr/LyricsGenius)
[![Documentation Status](https://readthedocs.org/projects/lyricsgenius/badge/?version=master)](https://lyricsgenius.readthedocs.io/en/latest/?badge=master)
[![PyPI version](https://badge.fury.io/py/lyricsgenius.svg)](https://pypi.org/project/lyricsgenius/)
[![Python version](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://pypi.org/project/lyricsgenius/)

`lyricsgenius` provides a simple interface to the song, artist, and lyrics data stored on [Genius.com](https://www.genius.com).

## Documentation

`lyricsgenius`'s full documentation is online at [Read the Docs](https://lyricsgenius.readthedocs.io/en/master/).

## Setup
Genius's API has two interaces: the developer's API and the tokenfree, undocumented public API. The developer's API has limited endpoints and needs a token (client- or user access token). On the other hand the public API is not limited and needs no token to work.
There are three ways to use the package:
* **With a user access token**: User access tokens provide the most functionality but they are really useful if you're planning to use Genius's [Web Annotator](https://genius.com/web-annotator). If you're not planning to use it (or don't even know what it is), that leaves you with using a client access token or no tokens.
* **With a client access token**: With a client access token you can get information using both the developers and the public API.
* **Without an access token**: Without an access token you won't be able to get information using the developers API, but the public API -which doesn't need a token- covers all of the developers API endpoints and many more! So you'll be okay.

Here's what you need to do for each approach:
- **To Get a User Access Tokens**:
    You need to sign up/log in on Genius, [create an app](http://genius.com/api-clients) and get a user token using OAuth2 (our [OAuth2](https://lyricsgenius.readthedocs.io/en/latest/reference/auth.html#auth) class can help you with that).
- **To Get a Client Access Token**:
    You need to sign up/log in on Genius and [create an app](http://genius.com/api-clients). Then on your app's page, click *GENERATE CLIENT ACCESS TOKEN* and you'll get a client access token.
- **No Token**:
    No need to do anything.


## Installation
`lyricsgenius` requires Python 3.

Use `pip` to install the package from PyPI:

```bash
pip install lyricsgenius
```

Or, install the latest version of the package from GitHub:

```bash
pip install git+https://github.com/johnwmillr/LyricsGenius.git
```

## Usage
Import the package and search for songs by a given artist:

```python
import lyricsgenius
genius = lyricsgenius.Genius(token) # or Genius()
artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title")
print(artist.songs)
```
By default, the `search_artist()` only returns songs where the given artist is the primary artist.
However, there may be instances where it is desirable to get all of the songs that the artist appears on.
You can do this by setting the `include_features` argument to `True`.

```python
artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title", include_features=True)
print(artist.songs)
```

Search for a single song by the same artist:

```python
song = artist.song("To You")
print(song.lyrics)
```

Add the song to the artist object:

```python
artist.add_song(song)
# the Artist object also accepts song names:
# artist.add_song("To You")
```

Save the artist's songs to a JSON file:

```python
artist.save_lyrics()
```

There are various options configurable as parameters within the `Genius` class:

```python
genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title
genius.public_api = False # Use the public API whenever possible (useful for token-less users)
```
Many methods have a `public_api` parameter that makes your client make the call using the public API. But as it can be inconvenient to set this parameter every time there is one, you can set `genius.public_api=True` and all methods that support it, will automatically make the call using the public API.

You can also call the package from the command line:

With a token:
```bash
export GENIUS_ACCESS_TOKEN="my_access_token_here"  # if you plan to use a token
python3 -m lyricsgenius --help
```
Without a token:
```bash
python3 -m lyricsgenius --help
```

Search for and save lyrics to a given song:

```bash
python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save
```

Search for five songs by 'The Beatles' and save the lyrics without a token:

```bash
python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save -tl
```

## Example projects

  - [Trucks and Beer: A textual analysis of popular country music](http://www.johnwmillr.com/trucks-and-beer/)
  - [Neural machine translation: Explaining the Meaning Behind Lyrics](https://github.com/tsandefer/dsi_capstone_3)
  - [What makes some blink-182 songs more popular than others?](http://jdaytn.com/posts/download-blink-182-data/)
  - [Sentiment analysis on hip-hop lyrics](https://github.com/Hugo-Nattagh/2017-Hip-Hop)
  - [Does Country Music Drink More Than Other Genres?](https://towardsdatascience.com/does-country-music-drink-more-than-other-genres-a21db901940b)
  - [49 Years of Lyrics: Why So Angry?](https://towardsdatascience.com/49-years-of-lyrics-why-so-angry-1adf0a3fa2b4)

## Contributing
Please contribute! If you want to fix a bug, suggest improvements, or add new features to the project, just [open an issue](https://github.com/johnwmillr/LyricsGenius/issues) or send me a pull request.
