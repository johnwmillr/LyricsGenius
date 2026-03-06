import lyricsgenius

genius = lyricsgenius.Genius()

song = genius.search_song("Dr Hansjakobli und ds Babettli", "Mani Matter")

song = genius.search_song("Dr Hansjakobli u ds Babettli", "Mani Matter")


if song is not None:
    print(song.lyrics)
    song.save_lyrics("/Users/john/Downloads/song.txt", extension="txt", overwrite=True)

song = genius.search_song("dua lipa", "new rules", False, False)
if song is not None:
    print(song.lyrics)
