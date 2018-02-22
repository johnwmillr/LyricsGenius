class Song(object):
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
        self._url      = self._body['url']
        self._api_path = self._body['api_path']
        self._id       = self._body['id']
                                                        
    @property
    def title(self):
        return str(self._body['title'].encode("utf-8", errors='ignore').decode("utf-8"))

    @property
    def artist(self):
        return str(self._body['primary_artist']['name'].encode("utf-8", errors='ignore').decode("utf-8"))

    @property
    def lyrics(self):
        return self._body['lyrics']
        
    @property
    def album(self):
        return self._body['album']['name']        
            
    @property
    def year(self):
        try:
            return self._body['release_date']
        except:
            return None
    
    @property
    def url(self):
        return self._body['url']
    
    @property
    def album_url(self):
        return self._body['album']['url']
    
    @property
    def featured_artists(self):
        return self._body['featured_artists']
    
    @property
    def media(self):
        m = {}
        if 'media' in self._body:
            [m.__setitem__(p['provider'],p['url']) for p in self._body['media']]
        return m
    
    @property
    def writer_artists(self):
        """List of artists credited as writers"""
        writers = []                
        [writers.append((writer['name'], writer['id'], writer['url'])) for writer in self._body['writer_artists']]
        return writers
    
    @property
    def song_art_image_url(self):
        try:
            return self._body['song_art_image_url']
        except:
            return None

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