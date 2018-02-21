# Scraping song lyrics from Genius.com

[![Build Status](https://travis-ci.org/johnwmillr/GeniusLyrics.svg?branch=master)](https://travis-ci.org/johnwmillr/GeniusLyrics)

## Setup
This repository is intended to provide an easy interface for programatically accessing the song information stored on [Genius.com](https://www.genius.com). Check out [my blog post](http://www.johnwmillr.com/scraping-genius-lyrics/) for a more thorough description of the package and its usage.

Start by cloning this repo:

```bash
git clone https://github.com/johnwmillr/LyricsGenius.git
```

To use the Genius API you'll need to sign up for a (free) client that authorizes you to [access their API](http://genius.com/api-clients). You'll need to supply the `client_access_token` that Genius gives you when using this module. See [Usage](https://github.com/johnwmillr/LyricsGenius#usage) below for an example.

You can read through the [Genius API docs](https://docs.genius.com/), but I've found it more helpful to start by looking at code folks have already written for the API. I found [this post](https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping) from @jackschultz and [this repository](https://github.com/jasonqng/genius-lyrics-search) from @JasonQNg real helpful while getting started, check their work out.  

## Installation
1. Clone this repo:  
`git clone https://github.com/johnwmillr/LyricsGenius.git`
2. Enter the directory created:  
`cd LyricsGenius`
3. Install using pip:  
`pip install .`

## Usage
```python
>>> import lyricsgenius as genius
>>> api = genius.Genius('my_client_access_token_here')
>>> artist = api.search_artist('Andy Shauf', max_songs=3)
Searching for Andy Shauf...

Song 1: "Alexander All Alone"
Song 2: "Begin Again"
Song 3: "Comfortable With Silence"

Reached user-specified song limit (3).
Found 3 songs.

Done.
>>> print(artist)
Andy Shauf, 3 songs
>>> song = api.search_song('To You',artist.name)
Searching for "To You" by Andy Shauf...
Done.
>>> print(song)
"To You" by Andy Shauf:
    Jeremy can we talk a minute?
    I've got some things that I need to
    Get off of my chestI know that we h...
>>> artist.add_song(song)
>>> print(artist)
Andy Shauf, 4 songs
```

You can also call the package from the command line.
```
$python -m lyricsgenius --search_song 'Begin Again' 'Andy Shauf'
$python -m lyricsgenius --search_artist 'Lupe Fiasco' 3
```

## Example projects
  
  - [Textual analysis of popular country music](http://www.johnwmillr.com/trucks-and-beer/)
  
  I'd love to have more examples to list here! Let me know if you've made use of this wrapper for one of your own projects, and I'll list it here.

## Contributing
Please contribute! I'd love to have collaborators on this project. If you want to add features, suggest improvements, or have other comments, just make a pull request or raise an issue.
