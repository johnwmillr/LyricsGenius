"""A library that provides a Python interface to the Genius.com API"""
__author__       = 'John W. Miller'
__url__          = 'https://github.com/johnwmillr/GeniusAPI'
__description__  = 'A Python wrapper around the Genius.com API'

#  -------------
#  Module usage:
#    from genius import Genius
#    G = Genius()
#    artist = G.search_artist('Andy Shauf',max_songs=5)
#    print(artist)
#
#    song = G.search_song('To You',artist.name)
#    artist.add_song(song)
#    print(artist)
#    print(artist.songs[-1])
#
#  -------------------
#  Command line usage:
#    python genius.py --search_song Yesterday 'The Beatles'
#
#    python genius.py --search_artist Common


import re
import requests
import json
from bs4 import BeautifulSoup
import urllib2
import socket

class _GeniusAPI(object):
    # This is a superclass that Genius() inherits from. Not sure if this makes any sense, but it
    # seemed like a good idea to have this class (more removed from user) handle the lower-level
    # interaction with the Genius API, and then Genius() has the more user-friendly search
    # functions
    """Interface with the Genius.com API
    
    Attributes:
        base_url: (str) Top-most URL to access the Genius.com API with
        
    Methods:
        _load_credentials()
            OUTPUT: client_id, client_secret, client_access_token
        _make_api_request()
            INPUT:  
            OUTPUT:                                 
    """    
    
    # Genius API constants
    _API_URL = "https://api.genius.com/"    
    _API_REQUEST_TYPES =\
        {'song': 'songs/', 'artist': 'artists/', 'artist-songs': 'artists/songs/','search': 'search?q='}
    
    def __init__(self):
        self._CLIENT_ACCESS_TOKEN = self._load_credentials()
        self._HEADER_AUTHORIZATION = 'Bearer ' + self._CLIENT_ACCESS_TOKEN        
        
    def _load_credentials(self):
        """Load the Genius.com API authorization information from the 'credentials.ini' file"""        
        lines = [str(line.rstrip('\n')) for line in open('credentials.ini')]        
        for line in lines:
            if "client_id" in line:
                client_id = line.split(": ")[1]
            if "client_secret" in line:
                client_secret = line.split(": ")[1]
            #Currently only need access token to run, the other two perhaps for future implementation
            if "client_access_token" in line:
                client_access_token = line.split(": ")[1]
                
        return client_access_token
    
    def _make_api_request(self, request_term_and_type, page=1):
        """Send a request (song, artist, or search) to the Genius API, returning a json object
        
        INPUT:
            request_term_and_type: (tuple) (request_term, request_type)
        
        *request term* is a string. If *request_type* is 'search', then *request_term* is just
        what you'd type into the search box on Genius.com. If you have an song ID or an artist ID,
        you'd do this: self._make_api_request('2236','song')
        
        Returns a json object.
        """        
        
        #The API request URL must be formatted according to the desired request type"""
        api_request = self._format_api_request(request_term_and_type,page=page)                
        
        # Add the necessary headers to the request
        request = urllib2.Request(api_request)        
        request.add_header("Authorization",self._HEADER_AUTHORIZATION)
        request.add_header("User-Agent","curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpnSSL 0.9.6b) (ipv6 enabled)")
        while True:
            try:
                response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
                raw = response.read()
            except socket.timeout:
                print("Timeout raised and caught")
                continue
            break

        return json.loads(raw)['response']
        
    def _format_api_request(self, term_and_type, page=1):
        """Format the request URL depending on the type of request"""            
        request_term, request_type = str(term_and_type[0]), term_and_type[1]                
        assert (request_type in self._API_REQUEST_TYPES), "Unknown API request type"
        
        # TODO - Clean this up (might not need separate returns)
        if request_type=='artist-songs':                        
            return self._API_URL + 'artists/' + urllib2.quote(request_term) + '/songs?per_page=50&page=' + str(page)
        else:        
            return self._API_URL + self._API_REQUEST_TYPES[request_type] + urllib2.quote(request_term)
    
    def _scrape_song_lyrics_from_url(self, URL):
        """Use BeautifulSoup to scrape song info off of a Genius song URL"""                                
        page = requests.get(URL)    
        html = BeautifulSoup(page.text, "html.parser")
        
        # Scrape the song lyrics from the HTML
        lyrics = html.find("div", class_="lyrics").get_text().encode('ascii','ignore').decode('ascii')
        lyrics = re.sub('\[.*\]','',lyrics) # Remove [Verse] and [Bridge] stuff
        lyrics = re.sub('\n{2}','',lyrics)  # Remove gaps between verses        
        lyrics = str(lyrics).strip('\n')
        
        return lyrics    
        

class Genius(_GeniusAPI):
    """User-level interface with the Genius.com API. User can search for songs (getting lyrics) and artists (getting songs)"""    
    
    def search_song(self, song_title, artist_name=''):
        """Search Genius.com for *song_title* by *artist_name*"""                
                    
        # Perform a Genius API search for the song
        if artist_name != '':            
            print('Searching for "{0}" by {1}...'.format(song_title,artist_name))
        else:            
            print('Searching for "{0}"...'.format(song_title))
        search_term = song_title + ' ' + artist_name
        json_search = self._make_api_request((search_term,'search'))        
                
        # Loop through search results, stopping as soon as title and artist of result match request
        n_hits = min(10,len(json_search['hits']))
        for i in range(n_hits):
            search_hit   = json_search['hits'][i]['result']
            found_title  = str(search_hit['title']).translate(None,' ').lower()
            found_artist = str(search_hit['primary_artist']['name']).translate(None,' ').lower()

            if found_title == song_title.translate(None,' ').lower() and (found_artist == artist_name.translate(None,' ').lower() or artist_name==''):
                # Found correct song, accessing API ID
                json_song = self._make_api_request((search_hit['id'],'song'))
                
                # Scrape the song's HTML for lyrics                
                lyrics = self._scrape_song_lyrics_from_url(json_song['song']['url'])

                # Create the Song object
                song = Song(json_song, lyrics)
                print('Done.\n')        
                return song
        
        print('Specified song was not first result :(')
        return None
        
    def search_artist(self, artist_name, get_songs=True, verbose=True, max_songs=None):
        """Allow user to search for an artist on the Genius.com database by supplying an artist name.
        Returns an Artist() object containing all songs for that particular artist."""
                                
        print('Searching for {0}...\n'.format(artist_name))
    
        # Perform a Genius API search for the artist                
        json_search = self._make_api_request((artist_name,'search'))                        
        for hit in json_search['hits']:                                          
            if str(hit['result']['primary_artist']['name']).lower()==artist_name.lower():                
                artist_id = str(hit['result']['primary_artist']['id'])                                                                
                break
            else:                                                            
                artist_id = None                                                                                        
        assert (not isinstance(artist_id,type(None))), "Could not find artist. Check spelling?"
        
        # Make Genius API request for the determined artist ID
        json_artist = self._make_api_request((artist_id,'artist'))

        # Create the Artist object
        artist = Artist(json_artist);
        
        if get_songs == True:            
            # Access the api_path found by searching
            artist_search_results = self._make_api_request((artist_id, 'artist-songs'))        

            # Download each song by artist, store as Song objects in Artist object
            keep_searching = True
            next_page = 0; n=0            
            while keep_searching:            
                for json_song in artist_search_results['songs']:
                    # Scrape song lyrics from the song's HTML
                    lyrics = self._scrape_song_lyrics_from_url(json_song['url'])            

                    # Create song object for current song
                    song = Song(json_song, lyrics)
                    if artist.add_song(song)==0:
                        n += 1
                        if verbose==True:
                            try: print('Song {0}: "{1}"'.format(n,song.title))
                            except: pass
                    
                    # Check if user specified a max number of songs for the artist
                    if not isinstance(max_songs,type(None)):
                        if artist.num_songs >= max_songs:
                            keep_searching = False
                            print('\nReached user-specified song limit ({0}).'.format(max_songs))
                            break

                # Move on to next page of search results
                next_page = artist_search_results['next_page']                
                if next_page == None:
                    break
                else: # Get next page of artist song results
                    artist_search_results = self._make_api_request((artist_id, 'artist-songs'), page=next_page)           

            print('Found {n_songs} songs.\n'.format(n_songs=artist.num_songs))

        print('Done.\n')
        return artist                    
    

class Song():    
    """A song from the Genius.com database.
    
    Attributes:
        title:  (str) Title of the song.
        artist: (str) Primary artist on the song.
        lyrcis: (str) Full set of song lyrics.
        album:  (str) Name of the album the song is on.
        year:   (int) Year the song was released.        
    """
                         
    def __init__(self, json_dict, lyrics=''):
        try: self._body = json_dict['song']
        except: self._body = json_dict
        self._body['lyrics'] = lyrics
        self._url      = str(self._body['url'])
        self._api_path = str(self._body['api_path'])
        self._id       = str(self._body['id'])  
                                                        
    @property
    def title(self):
        return str(self._body['title'])

    @property
    def artist(self):
        return str(self._body['primary_artist']['name'])

    @property
    def lyrics(self):
        return self._body['lyrics']
        
    @property
    def album(self):
        try: return str(self._body['album']['name'])
        except: return ''
            
    @property
    def year(self):
        return str(self._body['release_date'])
    
    @property
    def url(self):
        return str(self._body['url'])
    
    @property
    def album_url(self):
        return str(self._body['album']['url'])
    
    @property
    def featured_artists(self):
        return str(self._body['featured_artists'])
    
    @property
    def media(self):
        m = {}
        [m.__setitem__(p['provider'],p['url']) for p in self._body['media']]
        return m
    
    @property
    def writer_artists(self):
        """List of artists credited as writers"""
        writers = []
        [writers.append((str(writer['name']),str(writer['id']),str(writer['url'])))\
                        for writer in self._body['writer_artists']]
        return writers
    
    @property
    def song_art_image_url(self):
        return str(self._body['song_art_image_url'])

    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else: lyr = self.lyrics[:100]            
        return '"{title}" by {artist}:\n    {lyrics}'.format(title=self.title,artist=self.artist,lyrics=lyr.replace('\n','\n    '))       
    
    def __repr__(self):
        return repr((self.title, self.artist))
    
    def __cmp__(self, other):                        
        return cmp(self.title, other.title) and cmp(self.artist, other.artist) and cmp(self.lyrics, other.lyrics)
    
    def __list__(self):
        # How do I do this?
        return
                
class Artist():
    """An artist from the Genius.com database.
    
    Attributes:
        name: (str) Artist name.
        num_songs: (int) Total number of songs listed on Genius.com
    
    """                            

    def __init__(self, json_dict):
        """Populate the Artist object with the data from *json_dict*"""
        self._body = json_dict['artist']
        self._url      = str(self._body['url'])
        self._api_path = str(self._body['api_path'])
        self._id       = str(self._body['id']) 
        self._songs = []
        self._num_songs = len(self._songs)
        
    @property
    def name(self):
        return str(self._body['name'])
                    
    @property
    def image_url(self):
        return str(self._body['image_url'])        
    
    @property
    def songs(self):
        return self._songs
    
    @property
    def num_songs(self):
        return self._num_songs          
        
    def add_song(self, newsong):
        """Add a Song object to the Artist object"""
        
        if any([song.title==newsong.title for song in self._songs]):
            print('{newsong.title} already in {self.name}, not adding song.'.format(newsong=newsong,self=self))
        if newsong.artist == self.name:
            self._songs.append(newsong)
            self._num_songs += 1
            return 0 # Success
        else:
            print("Can't add song by {newsong.artist}, artist must be {self.name}.".format(newsong=newsong,self=self))
            return 1 # Failure        
            
    def get_song(self, song_name):
        """Search Genius.com for *song_name* and add it to artist"""
        song = Genius().search_song(song_name,self.name)
        self.add_song(song)
        return

    def __str__(self):
        """Return a string representation of the Artist object."""                        
        if self._num_songs == 1:
            return '{0}, {1} song'.format(self.name,self._num_songs)
        else:
            return '{0}, {1} songs'.format(self.name,self._num_songs)
    
    def __repr__(self):
        return repr((self.name, '{0} songs'.format(self._num_songs)))  




# --------------------------------------------------------------------
# Command line script functionality
#
#  Usage:
#    python genius.py --search_song Yesterday 'The Beatles'
#
#    python genius.py --search_artist Common

if __name__ == "__main__":
    import sys    
    G = Genius()    
                
    # There must be a standard way to handle "--" inputs on the command line
    if sys.argv[1] == '--search_song':            
        if len(sys.argv) == 4:                        
            song = G.search_song(sys.argv[2],sys.argv[3])
        elif len(sys.argv) == 3:
            song = G.search_song(sys.argv[2])                                
        print(song)
    elif sys.argv[1] == '--search_artist':
        artist = G.search_artist(sys.argv[2],get_songs=True,max_songs=10)
        print(artist)    
        
    print('\n')
    
         
    
    
    
    
    
    
    
    
    
    