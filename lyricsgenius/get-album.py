import pandas as pd
from bs4 import BeautifulSoup
import requests
import lyricsgenius as genius

# Get the token by signing in on the Genius website
client_access_token = 'CLIENTACCESSTOKEN'

# function to get the lyrics of an album in a json file using the lyricsgenius library


def search_album(artist_name, album_title):
    # authentify
    api = genius.Genius(client_access_token)
    # genius find the artist
    artist = api.search_artist(artist_name, max_songs=0)
    # modify artist_name and album_title so that they will lead us to the album page on Genius.com
    artist_name = artist_name.replace(" ", "-").replace(".", "").replace("$", "-").replace("\"", "").replace("'", "")
    album_title = album_title.replace(" ", "-").replace(".", "-").replace("$", "-").replace("'", "-").replace("\"", "-")
    while artist_name[-1] == '-':
        artist_name = artist_name[:-1]
    while album_title[-1] == '-':
        album_title = album_title[:-1]
    # create index
    index = []
    # get the album page on Genius.com
    r = requests.get('https://genius.com/albums/' + artist_name + "/" + album_title)
    soup = BeautifulSoup(r.text, 'html.parser')
    # get the html section indicating if the song is missing lyrics
    missing = soup.find_all('div', attrs={'class': 'chart_row-metadata_element chart_row-metadata_element--large'})
    miss_nb = 0
    # count the number of songs without lyrics
    for miss in missing:
        if miss.text.find("(Missing Lyrics)") >= 0:
            miss_nb = miss_nb + 1
    divi = soup.find_all('div', attrs={'class': 'column_layout-column_span column_layout-column_span--primary'})
    for div in divi:
        var = 0
        # get the html section indicating the track numbers (this will be to eliminate sections similar to those of songs but are actually of tracklist or credits of the album)
        mdiv = div.find_all('span', attrs={'class': 'chart_row-number_container-number chart_row-number_container-number--gray'})
        for mindiv in mdiv:
            nb = mindiv.text.replace("\n", "")
            if nb != "":
                index.append(nb)
        # create the pandas dataframe holding the tracks' titles
        df = pd.DataFrame(index=index, columns=['track_title'])
        ndiv = div.find_all('h3', attrs={'class': 'chart_row-content-title'})
        for mindiv in ndiv:
            tt = mindiv.text.replace("\n", "").strip()
            # getting rid of the featurings in the title
            if tt.find("(Ft") >= 0:
                tt = tt.split(" (Ft.", 1)[0]
            else:
                # getting ride of "lyrics" at the end of the title
                tt = tt.rsplit(" ", 1)[0].strip()
            df['track_title'][var] = tt
            var = var + 1
            if var == len(df.index):
                break
    # loop to add song with title from the dataframe
    for track in df['track_title']:
        # search the song
        song = api.search_song(track, artist.name)
        # if the song was found, it's added to artist
        if song != None:
            artist.add_song(song)
        # if the song wasn't found, it might be because it's formatted in this way : "title by other artist"
        elif track.find("by") >= 0:
            s_artist_name = track.replace("\xa0", " ").rsplit(" by ", 1)[1]
            s_artist = api.search_artist(s_artist_name, max_songs=0)
            track = track.replace("\xa0", " ").rsplit(" by ", 1)[0].strip()
            # look for song with other artist
            song = api.search_song(track, s_artist.name)
            if song != None:
                # add song to the album's main artist
                artist.add_song(song)
            else:
                print("Missing lyrics")
        else:
            print("Missing lyrics")
    artist.save_lyrics(format='json')
    if miss_nb == 1:
        print("{} song was ignored due to missing lyrics.".format(miss_nb))
    elif miss_nb > 1:
        print("{} songs were ignored due to missing lyrics.".format(miss_nb))


search_album("DJ Khaled", "Grateful")
