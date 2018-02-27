#  Command line usage:
#    $python3 -m lyricsgenius --search-song 'Begin Again' 'Andy Shauf'
#    $python3 -m lyricsgenius --search-artist 'Lupe Fiasco' 3

import sys
import os
import lyricsgenius as genius

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    
    client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
    assert client_access_token is not None, "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
    api = genius.Genius(client_access_token)
                
    # There must be a standard way to handle "--" inputs on the command line
    if sys.argv[1] == '--search-song':            
        if len(sys.argv) == 4:                        
            song = api.search_song(sys.argv[2],sys.argv[3])
        elif len(sys.argv) == 3:
            song = api.search_song(sys.argv[2])                                
        print('"{title}" by {artist}:\n    {lyrics}'.format(title=song.title,artist=song.artist,lyrics=song.lyrics.replace('\n','\n    ')))        
    elif sys.argv[1] == '--search-artist':
        if len(sys.argv) == 4:
            max_songs = int(sys.argv[3])
        else:
            max_songs = 5
        artist = api.search_artist(sys.argv[2], max_songs=max_songs)
        print("Saving {} lyrics...".format(artist.name))
        api.save_artist_lyrics(artist)
    else:
        print("Usage: python -m lyricsgenius [--search-song song_name] [--search-artist artist_name num_songs]")
        return

if __name__ == "__main__":
    main()