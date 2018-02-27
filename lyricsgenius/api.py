#  Usage:
#    import genius
#    api = genius.Genius('my_client_access_token_here')
#    artist = api.search_artist('Andy Shauf', max_songs=5)
#    print(artist)
#
#    song = api.search_song('To You', artist.name)
#    artist.add_song(song)
#    print(artist)
#    print(artist.songs[-1])

import sys
from urllib.request import Request, urlopen, quote # Python 3
import os, re
import requests, socket, json
from bs4 import BeautifulSoup
from string import punctuation

from .song import Song
from .artist import Artist

class _API(object):
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
    
    def __init__(self, client_access_token, client_secret='', client_id=''):        
        self._CLIENT_ACCESS_TOKEN = client_access_token
        self._HEADER_AUTHORIZATION = 'Bearer ' + self._CLIENT_ACCESS_TOKEN
           
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
        api_request = self._format_api_request(request_term_and_type, page=page)        
        
        # Add the necessary headers to the request
        request = Request(api_request)        
        request.add_header("Authorization", self._HEADER_AUTHORIZATION)
        request.add_header("User-Agent","")
        while True:
            try:
                response = urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
                raw = response.read().decode('utf-8')
            except socket.timeout:
                print("Timeout raised and caught")
                continue
            break
                                
        return json.loads(raw)['response']
        
    def _format_api_request(self, term_and_type, page=1):
        """Format the request URL depending on the type of request"""            

        request_term, request_type = str(term_and_type[0]), term_and_type[1]                
        assert request_type in self._API_REQUEST_TYPES, "Unknown API request type"
        
        # TODO - Clean this up (might not need separate returns)
        if request_type=='artist-songs':
            return self._API_URL + 'artists/' + quote(request_term) + '/songs?per_page=50&page=' + str(page)
        else:        
            return self._API_URL + self._API_REQUEST_TYPES[request_type] + quote(request_term)
    
    def _scrape_song_lyrics_from_url(self, URL):
        """Use BeautifulSoup to scrape song info off of a Genius song URL"""                                
        page = requests.get(URL)    
        html = BeautifulSoup(page.text, "html.parser")
        
        # Scrape the song lyrics from the HTML
        lyrics = html.find("div", class_="lyrics").get_text()
        lyrics = re.sub('\[.*\]',  '', lyrics) # Remove [Verse] and [Bridge] stuff
        lyrics = re.sub('\n{2}', '\n', lyrics) # Remove gaps between verses

        return lyrics.strip('\n')

    def _clean(self, s):
        return s.translate(str.maketrans('','',punctuation)).replace('\u200b', " ").strip()

class Genius(_API):
    """User-level interface with the Genius.com API. User can search for songs (getting lyrics) and artists (getting songs)"""    

    def search_song(self, song_title, artist_name=""):
        # TODO: Should search_song() be a @classmethod?
        """Search Genius.com for *song_title* by *artist_name*"""                
                    
        # Perform a Genius API search for the song
        if artist_name == "":
            print('Searching for "{0}" by {1}...'.format(song_title, artist_name))            
        else:            
            print('Searching for "{0}"...'.format(song_title))
        search_term = "{} {}".format(song_title, artist_name)
        
        json_search = self._make_api_request((search_term,'search'))        
                
        # Loop through search results, stopping as soon as title and artist of result match request
        n_hits = min(10,len(json_search['hits']))
        for i in range(n_hits):
            search_hit = json_search['hits'][i]['result']
            found_song   = self._clean(search_hit['title'])
            found_artist = self._clean(search_hit['primary_artist']['name'])
                                    
            # Download song from Genius.com if title and artist match the request
            if found_song == self._clean(song_title) and found_artist == self._clean(artist_name) or artist_name == "":
            
                # Found correct song, accessing API ID
                json_song = self._make_api_request((search_hit['id'],'song'))
                
                # Scrape the song's HTML for lyrics                
                lyrics = self._scrape_song_lyrics_from_url(json_song['song']['url'])

                # Create the Song object
                song = Song(json_song, lyrics)
                                
                print('Done.')
                return song
        
        print('Specified song was not first result :(')
        return None
        
    def search_artist(self, artist_name, verbose=True, max_songs=None):
        """Allow user to search for an artist on the Genius.com database by supplying an artist name.
        Returns an Artist() object containing all songs for that particular artist."""
                                
        print('Searching for {0}...\n'.format(artist_name))
    
        # Perform a Genius API search for the artist                
        json_search = self._make_api_request((artist_name,'search'))                        
        first_result, artist_id = None, None
        for hit in json_search['hits']:            
            found_artist = hit['result']['primary_artist']
            if first_result is None:
                first_result = found_artist
            artist_id = found_artist['id']
            if self._clean(found_artist['name'].lower()) == self._clean(artist_name.lower()):                
                break
            else:                
                # check for searched name in alternate artist names
                json_artist = self._make_api_request((artist_id, 'artist'))['artist']            
                if artist_name.lower() in [s.lower() for s in json_artist['alternate_names']]:
                    print("Found alternate name. Changing name to {}.".format(json_artist['name']))
                    artist_name = json_artist['name']
                    break
                artist_id = None
        
        if first_result is not None and artist_id is None and verbose:
            if input("Couldn't find {}. Did you mean {}? (y/n): ".format(artist_name, first_result['name'])).lower() == 'y':
                artist_name, artist_id = first_result['name'], first_result['id']
        assert (not isinstance(artist_id, type(None))), "Could not find artist. Check spelling?"
        
        # Make Genius API request for the determined artist ID
        json_artist = self._make_api_request((artist_id,'artist'))

        # Create the Artist object
        artist = Artist(json_artist);
        
        if max_songs is None or max_songs > 0:
            # Access the api_path found by searching
            artist_search_results = self._make_api_request((artist_id, 'artist-songs'))        

            # Download each song by artist, store as Song objects in Artist object
            keep_searching = True
            next_page = 0; n=0            
            while keep_searching:            
                for json_song in artist_search_results['songs']:
                    # TODO: Shouldn't I use self.search_song() here?
                    # Scrape song lyrics from the song's HTML
                    lyrics = self._scrape_song_lyrics_from_url(json_song['url'])            

                    # Create song object for current song
                    song = Song(self._make_api_request((json_song['id'], 'song')), lyrics)
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

        print('Done.')
        return artist

    def save_artist_lyrics(self, artist):
        n_songs = artist.num_songs
        filename = "Lyrics_" + artist.name.replace(" ","") + ".txt"                        
        with open(filename,'w') as lyrics_file:
            [lyrics_file.write(s.lyrics + 5*'\n') for s in artist.songs]
        print('Wrote lyrics for {} songs.'.format(n_songs))
