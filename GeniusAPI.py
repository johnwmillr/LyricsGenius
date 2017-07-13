# -*- coding: utf-8 -*-
"""
Python interface for the Genius API from Genius.com


Example usage: ::

    >>> import GeniusAPI as Genius
    >>> song1 = Genius.search_song('Yesterday','The Beatles')
    >>> song1.lyrics[:100]
    "Yesterday\nAll my troubles seemed so far away\nNow it looks as though they're here to stay\nOh, I belie"
    >>> song2 = Genius.search_song('Prom Night','Chance the Rapper')
    >>> print(song2)
    Prom Night, by Chance the Rapper:
    "Charlie Bartlett, John Bender
    Class Switcher, Time Bender
    Chance Bennett, a peculiar name
    Graduation..."
    >>> artist = Genius.search_artist('Michael Jackson')
    >>> artist.songs
    ['2000 Watts', '2 Bad', Ain't no sunshine', ...]
    
John W. Miller, @johwmillr
2017_0712
"""
    

class Artist(object):
    """An artist from the Genius.com database.
    
    Attributes:
        name: (str) Artist name.
        num_songs: (int) Total number of songs listed on Genius.com
    
    """
    def __init__(self, name, num_songs=0, song=None):
        """Return an Artist object whose name is *name*, etc."""
        self.name = name
        self.num_songs = num_songs
        self.songs = songs
                
    def add_song(self, song):
        """Add a Song object to the Artist object"""
        self.songs.append(song)
        self.num_songs += 1
        
    def remove_song(self, song):
        """Do I need this ability?"""
        
class Song(object):
    """A song from the Genius.com database.
    
    Attributes:
        title:  (str) Title of the song.
        artist: (str) Primary artist on the song.
        lyrcis: (str) Full set of song lyrics.
        album:  (str) Name of the album the song is on.
        year:   (int) Year the song was released.        
    """
    
    def __init__(self, title, artist, lyrics, album='',year=None):
        """Return a Song object whose title is *title*, artist is *artist*, and so on."""    

        self.title  = title
        self.artist = artist
        self.lyrics = lyrics
        self.album  = album
        self.year = year    
        
    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else: lyr = self.lyrics[:100]            
        return '{0}, by {1}:\n"{2}"'.format(self.title,self.artist,lyr)
    
    def __list__(self):
        # Is this a thing?
        return 
        