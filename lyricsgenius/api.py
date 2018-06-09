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
from urllib.request import Request, urlopen, quote
import os
import re
import requests
import socket
import json
from bs4 import BeautifulSoup
from string import punctuation
import time
from warnings import warn
import pandas as pd

from lyricsgenius.song import Song


class Artist(object):
    """An artist from the Genius.com database.

    Attributes:
        name: (str) Artist name.
        num_songs: (int) Total number of songs listed on Genius.com

    """

    def __init__(self, json_dict):
        """Populate the Artist object with the data from *json_dict*"""
        self._body = json_dict['artist']
        self._url = self._body['url']
        self._api_path = self._body['api_path']
        self._id = self._body['id']
        self._songs = []
        self._num_songs = len(self._songs)

    def __len__(self):
        return 1

    @property
    def name(self):
        return self._body['name']

    @property
    def image_url(self):
        try:
            return self._body['image_url']
        except:
            return None

    @property
    def songs(self):
        return self._songs

    @property
    def num_songs(self):
        return self._num_songs

    def add_song(self, newsong, verbose=True):
        """Add a Song object to the Artist object"""

        if any([song.title == newsong.title for song in self._songs]):
            if verbose:
                print('{newsong.title} already in {self.name}, not adding song.'.format(newsong=newsong, self=self))
            return 1  # Failure
        if newsong.artist == self.name:
            self._songs.append(newsong)
            self._num_songs += 1
            return 0  # Success
        else:
            self._songs.append(newsong)
            self._num_songs += 1
            print("Song by {newsong.artist} was added to {self.name}.".format(newsong=newsong, self=self))
            return 0  # Success

    def get_song(self, song_name):
        """Search Genius.com for *song_name* and add it to artist"""
        raise NotImplementedError("I need to figure out how to allow Artist() to access search_song().")
        song = Genius.search_song(song_name, self.name)
        self.add_song(song)
        return

    # TODO: define an export_to_json() method

    def save_lyrics(self, format='json', filename=None,
                    overwrite=False, skip_duplicates=True, verbose=True):
        """Allows user to save all lyrics within an Artist obejct to a .json or .txt file."""
        if format[0] == '.':
            format = format[1:]
        assert (format == 'json') or (format == 'txt'), "Format must be json or txt"

        # We want to reject songs that have already been added to artist collection
        def songsAreSame(s1, s2):
            from difflib import SequenceMatcher as sm  # For comparing similarity of lyrics
            # Idea credit: https://bigishdata.com/2016/10/25/talkin-bout-trucks-beer-and-love-in-country-songs-analyzing-genius-lyrics/
            seqA = sm(None, s1.lyrics, s2['lyrics'])
            seqB = sm(None, s2['lyrics'], s1.lyrics)
            return seqA.ratio() > 0.5 or seqB.ratio() > 0.5

        def songInArtist(new_song):
            # artist_lyrics is global (works in Jupyter notebook)
            for song in lyrics_to_write['songs']:
                if songsAreSame(new_song, song):
                    return True
            return False

        # Determine the filename
        if filename is None:
            filename = "Lyrics_{}.{}".format(self.name.replace(" ", ""), format)
        else:
            if filename.rfind('.') != -1:
                filename = filename[filename.rfind('.'):] + '.' + format
            else:
                filename = filename + '.' + format

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
            lyrics_to_write = {'songs': [], 'artist': self.name}
            for song in self.songs:
                if skip_duplicates is False or not songInArtist(song):  # This takes way too long! It's basically O(n^2), can I do better?
                    lyrics_to_write['songs'].append({})
                    lyrics_to_write['songs'][-1]['title'] = song.title
                    lyrics_to_write['songs'][-1]['album'] = song.album
                    lyrics_to_write['songs'][-1]['year'] = song.year
                    lyrics_to_write['songs'][-1]['lyrics'] = song.lyrics
                    lyrics_to_write['songs'][-1]['image'] = song.song_art_image_url
                    lyrics_to_write['songs'][-1]['artist'] = self.name
                    lyrics_to_write['songs'][-1]['raw'] = song._body
                else:
                    if verbose:
                        print("SKIPPING \"{}\" -- already found in artist collection.".format(song.title))
        else:
            lyrics_to_write = " ".join([s.lyrics + 5 * '\n' for s in self.songs])

        # Write the lyrics to either a .json or .txt file
        if write_file:
            with open(filename, 'w') as lyrics_file:
                if format == 'json':
                    json.dump(lyrics_to_write, lyrics_file)
                else:
                    lyrics_file.write(lyrics_to_write)
            if verbose:
                print('Wrote {} songs to {}.'.format(self.num_songs, filename))
        else:
            if verbose:
                print('Skipping file save.\n')
        return lyrics_to_write

    def __str__(self):
        """Return a string representation of the Artist object."""
        if self._num_songs == 1:
            return '{0}, {1} song'.format(self.name, self._num_songs)
        else:
            return '{0}, {1} songs'.format(self.name, self._num_songs)

    def __repr__(self):
        return repr((self.name, '{0} songs'.format(self._num_songs)))


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
        {'song': 'songs/', 'artist': 'artists/',
            'artist-songs': 'artists/songs/', 'search': 'search?q='}

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

        # TODO: This should maybe be a generator

        # The API request URL must be formatted according to the desired
        # request type"""
        api_request = self._format_api_request(
            request_term_and_type, page=page)

        # Add the necessary headers to the request
        request = Request(api_request)
        request.add_header("Authorization", self._HEADER_AUTHORIZATION)
        request.add_header("User-Agent", "LyricsGenius")
        while True:
            try:
                # timeout set to 4 seconds; automatically retries if times out
                response = urlopen(request, timeout=4)
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
        if request_type == 'artist-songs':
            return self._API_URL + 'artists/' + quote(request_term) + '/songs?per_page=50&page=' + str(page)
        else:
            return self._API_URL + self._API_REQUEST_TYPES[request_type] + quote(request_term)

    def _scrape_song_lyrics_from_url(self, URL, remove_section_headers=False):
        """Use BeautifulSoup to scrape song info off of a Genius song URL"""
        page = requests.get(URL)
        html = BeautifulSoup(page.text, "html.parser")

        # Scrape the song lyrics from the HTML
        lyrics = html.find("div", class_="lyrics").get_text()
        if remove_section_headers:
            # Remove [Verse] and [Bridge] stuff
            lyrics = re.sub('(\[.*?\])*', '', lyrics)
            # Remove gaps between verses
            lyrics = re.sub('\n{2}', '\n', lyrics)

        return lyrics.strip('\n')

    def _clean_str(self, s):
        return s.translate(str.maketrans('', '', punctuation)).replace('\u200b', " ").strip().lower()

    def _result_is_lyrics(self, song_title):
        """Returns False if result from Genius is not actually song lyrics"""
        regex = re.compile(
            r"(tracklist)|(track list)|(album art(work)?)|(liner notes)|(booklet)|(credits)", re.IGNORECASE)
        return not regex.search(song_title)


class Genius(_API):
    """User-level interface with the Genius.com API. User can search for songs (getting lyrics) and artists (getting songs)"""

    def search_song(self, song_title, artist_name="", take_first_result=False, verbose=True, remove_section_headers=False, remove_non_songs=True):
        # TODO: Should search_song() be a @classmethod?
        """Search Genius.com for *song_title* by *artist_name*"""

        # Perform a Genius API search for the song
        if verbose:
            if artist_name != "":
                print('Searching for "{0}" by {1}...'.format(
                    song_title, artist_name))
            else:
                print('Searching for "{0}"...'.format(song_title))
        search_term = "{} {}".format(song_title, artist_name)

        json_search = self._make_api_request((search_term, 'search'))

        # Loop through search results, stopping as soon as title and artist of
        # result match request
        n_hits = min(10, len(json_search['hits']))
        for i in range(n_hits):
            search_hit = json_search['hits'][i]['result']
            found_song = self._clean_str(search_hit['title'])
            found_artist = self._clean_str(
                search_hit['primary_artist']['name'])

            # Download song from Genius.com if title and artist match the request
            if take_first_result or found_song == self._clean_str(song_title) and found_artist == self._clean_str(artist_name) or artist_name == "":

                # Remove non-song results (e.g. Linear Notes, Tracklists, etc.)
                song_is_valid = self._result_is_lyrics(found_song) if remove_non_songs else True
                if song_is_valid:
                    # Found correct song, accessing API ID
                    json_song = self._make_api_request((search_hit['id'], 'song'))

                    # Scrape the song's HTML for lyrics
                    lyrics = self._scrape_song_lyrics_from_url(json_song['song']['url'], remove_section_headers)

                    # Create the Song object
                    song = Song(json_song, lyrics)

                    if verbose:
                        print('Done.')
                    return song
                else:
                    if verbose:
                        print('Specified song does not contain lyrics. Rejecting.')
                    return None

        if verbose:
            print('Specified song was not first result :(')
        return None

    def search_artist(self, artist_name, verbose=True, max_songs=None, take_first_result=False, get_full_song_info=True, remove_section_headers=False, remove_non_songs=True):
        """Allow user to search for an artist on the Genius.com database by supplying an artist name.
        Returns an Artist() object containing all songs for that particular artist."""

        if verbose:
            print('Searching for songs by {0}...\n'.format(artist_name))

        # Perform a Genius API search for the artist
        json_search = self._make_api_request((artist_name, 'search'))
        first_result, artist_id = None, None
        for hit in json_search['hits']:
            found_artist = hit['result']['primary_artist']
            if first_result is None:
                first_result = found_artist
            artist_id = found_artist['id']
            if take_first_result or self._clean_str(found_artist['name'].lower()) == self._clean_str(artist_name.lower()):
                artist_name = found_artist['name']
                break
            else:
                # check for searched name in alternate artist names
                json_artist = self._make_api_request((artist_id, 'artist'))['artist']
                if artist_name.lower() in [s.lower() for s in json_artist['alternate_names']]:
                    if verbose:
                        print("Found alternate name. Changing name to {}.".format(json_artist['name']))
                    artist_name = json_artist['name']
                    break
                artist_id = None

        if first_result is not None and artist_id is None and verbose:
            if input("Couldn't find {}. Did you mean {}? (y/n): ".format(artist_name, first_result['name'])).lower() == 'y':
                artist_name, artist_id = first_result['name'], first_result['id']
        assert (not isinstance(artist_id, type(None))), "Could not find artist. Check spelling?"

        # Make Genius API request for the determined artist ID
        json_artist = self._make_api_request((artist_id, 'artist'))
        # Create the Artist object
        artist = Artist(json_artist)

        if max_songs is None or max_songs > 0:
            # Access the api_path found by searching
            artist_search_results = self._make_api_request((artist_id, 'artist-songs'))

            # Download each song by artist, store as Song objects in Artist object
            keep_searching = True
            next_page = 0
            n = 0
            while keep_searching:
                for json_song in artist_search_results['songs']:
                    # TODO: Shouldn't I use self.search_song() here?

                    # Songs must have a title
                    if 'title' not in json_song:
                        json_song['title'] = 'MISSING TITLE'

                    # Remove non-song results (e.g. Linear Notes, Tracklists, etc.)
                    song_is_valid = self._result_is_lyrics(json_song['title']) if remove_non_songs else True

                    if song_is_valid:
                        # Scrape song lyrics from the song's HTML
                        lyrics = self._scrape_song_lyrics_from_url(json_song['url'], remove_section_headers)

                        # Create song object for current song
                        if get_full_song_info:
                            song = Song(self._make_api_request((json_song['id'], 'song')), lyrics)
                        else:
                            song = Song({'song': json_song}, lyrics)  # Faster, less info from API

                        # Add song to the Artist object
                        if artist.add_song(song, verbose=False) == 0:
                            # print("Add song: {}".format(song.title))
                            n += 1
                            if verbose:
                                print('Song {0}: "{1}"'.format(n, song.title))

                    else:  # Song does not contain lyrics
                        if verbose:
                            print('"{title}" does not contain lyrics. Rejecting.'.format(title=json_song['title']))

                    # Check if user specified a max number of songs for the artist
                    if not isinstance(max_songs, type(None)):
                        if artist.num_songs >= max_songs:
                            keep_searching = False
                            if verbose:
                                print('\nReached user-specified song limit ({0}).'.format(max_songs))
                            break

                # Move on to next page of search results
                next_page = artist_search_results['next_page']
                if next_page == None:
                    break
                else:  # Get next page of artist song results
                    artist_search_results = self._make_api_request((artist_id, 'artist-songs'), page=next_page)

            if verbose:
                print('Found {n_songs} songs.'.format(n_songs=artist.num_songs))

        if verbose:
            print('Done.')

        return artist

    def search_album(self, artist_name, album_title):
        """Get all lyrics from an album"""
        # authentify
        api = Genius(client_access_token)
        # genius find the artist
        artist = api.search_artist(artist_name, max_songs=0)
        # modify artist_name and album_title so that they will lead us to the album page on Genius.com
        for ch in [',', "/", ' ', '$', ';', ':', '(', ')', '[', ']', '----', '---', '--']:
            if ch in artist._body['name']:
                artist_name = artist._body['name'].replace(ch, "-")
            if ch in album_title:
                album_title = album_title.replace(ch, "-")

        for ch in ['.', "\"", "'"]:
            if ch in artist_name:
                artist_name = artist_name.replace(ch, "")
            if ch in album_title:
                album_title = album_title.replace(ch, "-")

        for ch in ['é', 'è', 'ê', 'ë']:
            if ch in artist_name:
                artist_name = artist_name.replace(ch, "e")
            if ch in album_title:
                album_title = album_title.replace(ch, "e")

        artist_name = artist_name.replace("&", "and")
        album_title = album_title.replace("&", "").replace("#", "").replace("--", "-")

        while artist_name[-1] == '-':
            artist_name = artist_name[:-1]
        while album_title[-1] == '-':
            album_title = album_title[:-1]
        # create index
        index = []
        # get the album page on Genius.com
        r = requests.get('https://genius.com/albums/' + artist_name + "/" + album_title)
        soup = BeautifulSoup(r.text, 'html.parser')
        # get the html section indicating if the album isn't found
        not_found = soup.find('h1', attrs={'class': 'render_404-headline'})
        if not_found != None and "Page not found" in not_found.text:
            print("Album not found.")
            return None
        # get the html section indicating if the song is missing lyrics
        missing = soup.find_all('div', attrs={'class': 'chart_row-metadata_element chart_row-metadata_element--large'})
        miss_nb = 0
        # count the number of songs without lyrics
        for miss in missing:
            if miss.text.find("(Missing Lyrics)") >= 0 or miss.text.find("(Unreleased)") >= 0:
                miss_nb += 1
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
                var += 1
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

    def save_artists(self, artists, filename="artist_lyrics", overwrite=False):
        """Pass a list of Artist objects to save multiple artists"""
        if isinstance(artists, Artist):
            artists = [artists]
        assert isinstance(artists, list), "Must pass in list of Artist objects."

        # Create a temporary directory for lyrics
        start = time.time()
        tmp_dir = 'tmp_lyrics'
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
            tmp_count = 0
        else:
            tmp_count = len(os.listdir('./' + tmp_dir))

        # Check if file already exists
        write_file = False
        if not os.path.isfile(filename + ".json"):
            pass
        elif overwrite:
            pass
        else:
            if input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower() != 'y':
                print("Leaving file in place. Exiting.")
                os.rmdir(tmp_dir)
                return

        # Extract each artist's lyrics in json format
        all_lyrics = {'artists': []}
        for n, artist in enumerate(artists):
            if isinstance(artist, Artist):
                all_lyrics['artists'].append({})
                tmp_file = "./{dir}/tmp_{num}_{name}".format(dir=tmp_dir, num=n + tmp_count, name=artist.name.replace(" ", ""))
                print(tmp_file)
                all_lyrics['artists'][-1] = artist.save_lyrics(filename=tmp_file, overwrite=True)
            else:
                warn("Item #{} was not of type Artist. Skipping.".format(n))

        # Save all of the lyrics
        with open(filename + '.json', 'w') as outfile:
            json.dump(all_lyrics, outfile)

        end = time.time()


# Get the token by signing in on the Genius website https://genius.com/api-clients   (free)
client_access_token = 'xGTE6BWS9yG0EQ4D2RLefoKyjbj3d1SPfUgiA8ifk_bmKj24xhf7GO3iMPlPtB0b'
api = Genius(client_access_token)

Genius.search_album(api, "Ace Hood", "Trials & Tribulations")
