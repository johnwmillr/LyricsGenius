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

from genius.song import Song
from genius.artist import Artist