import lyricsgenius
genius = lyricsgenius.Genius("8JuZA2LLElhUEwq_NW25t46s5oLYqjNhTXRoUxKmRENwH8LnWzorrhKl-thRS7E3")
artist = genius.search_artist("EMINEM", max_songs=1, sort="title")
# print(artist.songs)
song = genius.search_song("cleanin out my closet", artist.name)
print(song.lyrics)



"""
To get referents : referents?song_id=id

From the returned JSON we have array of referents in ["response"]["referents"]

From a referent we have annotations id in ["annotations"][annotation_indice]["id"]
"""

# 