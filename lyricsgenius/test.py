from lyricsgenius.api import Genius
genius = Genius("8JuZA2LLElhUEwq_NW25t46s5oLYqjNhTXRoUxKmRENwH8LnWzorrhKl-thRS7E3")
artist = genius.search_artist("EMINEM", max_songs=1, sort="title")
# print(artist.songs)
song = genius.search_song("cleanin out my closet", artist.name)
print(song.lyrics)

anno = genius.get_annotations(song._id)
print(len(anno))