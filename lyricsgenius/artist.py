import json, os
try:
    input = raw_input # python 2
except:
    pass

class Artist(object):
    """An artist from the Genius.com database.
    
    Attributes:
        name: (str) Artist name.
        num_songs: (int) Total number of songs listed on Genius.com
    
    """                            

    def __init__(self, json_dict):
        """Populate the Artist object with the data from *json_dict*"""
        self._body = json_dict['artist']
        self._url      = self._body['url']
        self._api_path = self._body['api_path']
        self._id       = self._body['id']
        self._songs = []
        self._num_songs = len(self._songs)
        
    @property
    def name(self):            
        return str(self._body['name'].encode("utf-8", errors='ignore').decode("utf-8"))
                    
    @property
    def image_url(self):
        return self._body['image_url']
    
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
            return 1 # Failure
        if newsong.artist == self.name:
            self._songs.append(newsong)
            self._num_songs += 1
            return 0 # Success
        else:
            print("Can't add song by {newsong.artist}, artist must be {self.name}.".format(newsong=newsong,self=self))
            return 1 # Failure        
            
    def get_song(self, song_name):
        """Search Genius.com for *song_name* and add it to artist"""        
        raise NotImplementedError("I need to figure out how to allow Artist() to access search_song().")
        song = Genius.search_song(song_name,self.name)
        self.add_song(song)
        return

    def save_lyrics(self, format='json', filename=None, overwrite=False):
        """Allows user to save all lyrics within an Artist obejct to a .json or .txt file."""
        assert (format == 'json') or (format == 'txt'), "Format must be json or txt"

        # Determine the filename
        if filename is None:
            filename = "Lyrics_{}.{}".format(self.name.replace(" ",""), format)
        else:
            filename = filename.split('.')[0] + '.' + format
            
        # Check if file already exists    
        write_file = False
        if not os.path.isfile(filename):
            write_file = True
        elif overwrite:
            write_file = True
        else:
            if input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower() == 'y':
                write_file = True
                
        # Format lyrics in either .txt or .json format
        if format == 'json':
            raise NotImplementedError
        else:
            lyrics_to_write = " ".join([s.lyrics + 5*'\n' for s in self.songs])

        # Write the lyrics to either a .json or .txt file
        if write_file:
            try:
                with open(filename, 'w') as lyrics_file:
                    lyrics_file.write(lyrics_to_write)
                print('Wrote {} songs to {}.'.format(self.num_songs, filename))
            except:
                raise # TODO: Not sure if this how to do it
        else:
            print('Skipping file save.\n')

    def __str__(self):
        """Return a string representation of the Artist object."""                        
        if self._num_songs == 1:
            return '{0}, {1} song'.format(self.name,self._num_songs)
        else:
            return '{0}, {1} songs'.format(self.name,self._num_songs)
    
    def __repr__(self):
        return repr((self.name, '{0} songs'.format(self._num_songs))) 