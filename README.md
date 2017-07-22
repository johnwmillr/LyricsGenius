# Scraping song lyrics from Genius.com

## Setup
This repository is intended to provide an easy interface for programatically accessing the song information stored on [Genius.com](https://www.genius.com). Start by cloning this repo:

```bash
git clone https://github.com/johnwmillr/GeniusAPI.git
```

To use the Genius API you'll need to sign up for a (free) client that authorizes you to [access their API](http://genius.com/api-clients). Fill out the ```credentials.ini``` file using the API client info you were assigned.


You can read through the [Genius API docs](https://docs.genius.com/), but I've found it more helpful to start by looking at code folks have already written for the API. I found [this post](https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping) from @jackschultz and [this repository](https://github.com/jasonqng/genius-lyrics-search) from @JasonQNg real helpful while getting started, check their work out.


## Scraping lyrics
I'm most interested in a simple interface for pulling song lyrics from the website. It'd be nice to be able to enter a song and artist name and have the lyrics saved to a text file. Maybe we'd be interested in getting all lyrics associated with a single artist.

Genius doesn't actually provide a way to access the lyrics using their API directly ([they have to pay royalties on the lyrics](https://www.nytimes.com/2014/05/07/business/media/rap-genius-website-agrees-to-license-with-music-publishers.html?ref=oembed&_r=0)), but it doesn't take much more work to scrape the HTML after finding the song URLs we're interested in. The python functions below both start by using the Genius API to search for a song's URL and then scraping that URL for lyrics using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

## Usage
### Python module
```python
from genius import Genius
G = Genius()

artist = G.search_artist('Andy Shauf',max_songs=5)
print(artist)

song = G.search_song('To You',artist.name)
artist.add_song(song)

print(artist)
print(artist.songs[-1])
```

### Command line
```
python genius.py --search_song 'Begin Again' 'Andy Shauf'

python genius.py --search_artist 'Common'
```

