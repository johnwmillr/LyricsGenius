# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

"""
API documentation: https://docs.genius.com/
"""

import os
import re
import requests
import shutil
import socket
import json
from bs4 import BeautifulSoup
from string import punctuation
import time
from warnings import warn

from .song import Song
from .artist import Artist


class API(object):
    """Genius API"""

    # Create a persistent requests connection
    _session = requests.Session()
    _session.headers = {'application': 'LyricsGenius',
       'User-Agent': 'https://github.com/johnwmillr/LyricsGenius'}

    def __init__(self, client_access_token,
                 response_format='plain', timeout=5, sleep_time=0.5):
        """ Genius API Constructor

        :param client_access_token: API key provided by Genius
        :param response_format: API response format (dom, plain, html)
        :param timeout: time before quitting on response (seconds)
        :param sleep_time: time to wait between requests
        """

        self._ACCESS_TOKEN = client_access_token
        self._session.headers['authorization'] = 'Bearer ' + self._ACCESS_TOKEN
        self.response_format = response_format.lower()
        self.api_root = 'https://api.genius.com/'
        self.timeout = timeout
        self.sleep_time = sleep_time

    def _make_request(self, path, method='GET', params_=None):
        """Make a request to the API"""

        uri = self.api_root + path
        if params_:
            params_['text_format'] = self.response_format
        else:
            params_ = {'text_format': self.response_format}

        # Make the request
        try:
            response = self._session.request(method, uri,
                                            timeout=self.timeout,
                                            params=params_)
        except socket.timeout as e:
            print("Timeout raised and caught: {}".format(e))

        time.sleep(self.sleep_time)
        return response.json()['response']

    def get_song(self, id_):
        """Data for a specific song."""
        endpoint = "songs/{id}".format(id=id_)
        return self._make_request(endpoint)

    def get_artist(self, id_):
        """Data for a specific artist."""
        endpoint = "artists/{id}".format(id=id_)
        return self._make_request(endpoint)

    def get_artist_songs(self, id_, sort='title', per_page=20, page=1):
        """Documents (songs) for the artist specified."""
        endpoint = "artists/{id}/songs".format(id=id_)
        params = {'sort': sort, 'per_page': per_page, 'page': page}
        return self._make_request(endpoint, params_=params)

    def search_genius(self, search_term):
        """Search documents hosted on Genius."""
        endpoint = "search/"
        params = {'q': search_term}
        return self._make_request(endpoint, params_=params)

    def get_annotation(self, id_):
        """Data for a specific annotation."""
        endpoint = "annotations/{id}".format(id=id_)
        return self._make_request(endpoint)


class Genius(API):
    """User-level interface with the Genius.com API."""

    def __init__(self, client_access_token,
                 response_format='plain', timeout=5, sleep_time=0.5,
                 verbose=True, remove_section_headers=False,
                 skip_non_songs=True, take_first_result=False,
                 excluded_terms=[], replace_default_terms=False):
        """ Genius Client Constructor

        :param verbose: Turn printed messages on or off (bool)
        :param remove_section_headers: If True, removes [Chorus], [Bridge], etc. headers from lyrics
        :param skip_non_songs: If True, attempts to skip non-songs (e.g. track listings)
        :param take_first_result: Force searches to choose first result
        :param excluded_terms: (list) extra terms for flagging results as non-lyrics
        :param replace_default_terms: if True, replaces default excluded terms with user's
        """

        super().__init__(client_access_token, response_format, timeout, sleep_time)
        self.verbose = verbose
        self.remove_section_headers = remove_section_headers
        self.skip_non_songs = skip_non_songs
        self.take_first_result = take_first_result
        self.excluded_terms = excluded_terms
        self.replace_default_terms = replace_default_terms

    def _scrape_song_lyrics_from_url(self, URL):
        """Use BeautifulSoup to scrape song info off of a Genius song URL"""
        page = requests.get(URL)
        if page.status_code == 404:
            return None

        # Scrape the song lyrics from the HTML
        html = BeautifulSoup(page.text, "html.parser")
        lyrics = html.find("div", class_="lyrics").get_text()
        if self.remove_section_headers:  # Remove [Verse], [Bridge], etc.
            lyrics = re.sub('(\[.*?\])*', '', lyrics)
            lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses

        return lyrics.strip('\n')

    def _clean_str(self, s):
        return s.translate(str.maketrans('', '', punctuation)).replace('\u200b', " ").strip().lower()

    def _result_is_lyrics(self, song_title):
        """Returns False if result from Genius is not actually song lyrics
            Set the `excluded_terms` and `replace_default_terms` as
            instance variables within the Genius class.
        """

        default_terms = ['track\\s?list', 'album art(work)?', 'liner notes',
                         'booklet', 'credits', 'interview', 'skit',
                         'instrumental']
        if self.excluded_terms:
            if self.replace_default_terms:
                default_terms = self.excluded_terms
            else:
                default_terms.extend(self.excluded_terms)

        expression = r"".join(["({})|".format(term) for term in default_terms]).strip('|')
        regex = re.compile(expression, re.IGNORECASE)
        return not regex.search(song_title)

    def search_song(self, song_title, artist_name=""):
        """Search Genius.com for *song_title* by *artist_name*

        :param song_title: Song title to search for
        :param artist_name: Name of the artist (optional)

        # TODO: Should search_song() be a @classmethod?
        """

        # Perform a Genius API search for the song
        if self.verbose:
            if artist_name != "":
                print('Searching for "{0}" by {1}...'.format(
                    song_title, artist_name))
            else:
                print('Searching for "{0}"...'.format(song_title))
        search_term = "{} {}".format(song_title, artist_name)

        json_search = self.search_genius(search_term)

        # Loop through search results
        # Stop as soon as title and artist of result match request
        n_hits = min(10, len(json_search['hits']))
        for i in range(n_hits):
            search_hit = json_search['hits'][i]['result']
            found_song = self._clean_str(search_hit['title'])
            found_artist = self._clean_str(
                search_hit['primary_artist']['name'])

            # Download song if title and artist match search request
            if (self.take_first_result or
                found_song == self._clean_str(song_title) and
                found_artist == self._clean_str(artist_name) or
                artist_name == ""):

                # Remove non-song results (e.g. Linear Notes, Tracklists, etc.)
                song_is_valid = self._result_is_lyrics(found_song) if self.skip_non_songs else True
                if song_is_valid:
                    # Found correct song, accessing API ID
                    json_song = self.get_song(search_hit['id'])

                    # Scrape the song's HTML for lyrics
                    lyrics = self._scrape_song_lyrics_from_url(json_song['song']['url'])

                    # Remove results where the URL returns a 404 or lyrics can't be found
                    if lyrics:
                        song = Song(json_song, lyrics)
                        if self.verbose:
                            print('Done.')
                        return song
                    else:
                        if self.verbose:
                            print('Specified song does not have a valid URL with lyrics. Rejecting.')
                        return None
                else:
                    if self.verbose:
                        print('Specified song does not contain lyrics. Rejecting.')
                    return None

        if self.verbose:
            print('Specified song was not first result')
        return None

    def search_artist(self, artist_name, max_songs=None, get_full_song_info=True):
        """Search Genius.com for songs by the specified artist.
        Returns an Artist object containing artist's songs.
        :param artist_name: Name of the artist to search for
        :param max_songs: Maximum number of songs to search for
        :param get_full_song_info: Get full info for each song (slower)
        """

        if self.verbose:
            print('Searching for songs by {0}...\n'.format(artist_name))

        # Perform a Genius API search for the artist
        json_search = self.search_genius(artist_name)
        first_result, artist_id = None, None
        for hit in json_search['hits']:
            found_artist = hit['result']['primary_artist']
            if first_result is None:
                first_result = found_artist
            artist_id = found_artist['id']
            if (self.take_first_result or
                self._clean_str(found_artist['name'].lower()) ==
                self._clean_str(artist_name.lower())):
                # Break out if desired artist is found
                artist_name = found_artist['name']
                break
            else:
                # check for searched name in alternate artist names
                json_artist = self.get_artist(artist_id)['artist']
                if artist_name.lower() in [s.lower() for s in json_artist['alternate_names']]:
                    if self.verbose:
                        print("Found alternate name. Changing name to {}.".format(json_artist['name']))
                    artist_name = json_artist['name']
                    break
                artist_id = None

        if first_result is not None and artist_id is None and self.verbose:
            if input("Couldn't find {}. Did you mean {}? (y/n): ".format(artist_name,
                                                         first_result['name'])).lower() == 'y':
                artist_name, artist_id = first_result['name'], first_result['id']
        assert (not isinstance(artist_id, type(None))), "Could not find artist. Check spelling?"

        # Make Genius API request for the determined artist ID
        json_artist = self.get_artist(artist_id)
        # Create the Artist object
        artist = Artist(json_artist)

        if max_songs is None or max_songs > 0:
            # Access the api_path found by searching
            artist_search_results = self.get_artist_songs(artist_id)

            # Download each song by artist, store as Song objects in Artist object
            keep_searching = True
            next_page, n = 0, 0
            while keep_searching:
                for json_song in artist_search_results['songs']:
                    # TODO: Shouldn't I use self.search_song() here?

                    # Songs must have a title
                    if 'title' not in json_song:
                        json_song['title'] = 'MISSING TITLE'

                    # Remove non-song results (e.g. Linear Notes, Tracklists, etc.)
                    lyrics = self._scrape_song_lyrics_from_url(json_song['url'])
                    song_is_valid = self._result_is_lyrics(json_song['title']) if (lyrics and self.skip_non_songs) else True

                    if song_is_valid:
                        if get_full_song_info:
                            song = Song(self.get_song(json_song['id']), lyrics)
                        else:  # Create song with less info (faster)
                            song = Song({'song': json_song}, lyrics)

                        # Add song to the Artist object
                        if artist.add_song(song, verbose=False) == 0:
                            n += 1
                            if self.verbose:
                                print('Song {0}: "{1}"'.format(n, song.title))

                    else:  # Song does not contain lyrics
                        if self.verbose:
                            print('"{title}" does not contain lyrics. Rejecting.'.format(title=json_song['title']))

                    # Check if user specified a max number of songs
                    if not isinstance(max_songs, type(None)):
                        if artist.num_songs >= max_songs:
                            keep_searching = False
                            if self.verbose:
                                print('\nReached user-specified song limit ({0}).'.format(max_songs))
                            break

                # Move on to next page of search results
                next_page = artist_search_results['next_page']
                if next_page is None:
                    break
                else:  # Get next page of artist song results
                    artist_search_results = self.get_artist_songs(artist_id, page=next_page)

            if self.verbose:
                print('Found {n_songs} songs.'.format(n_songs=artist.num_songs))

        if self.verbose:
            print('Done.')

        return artist

    def save_artists(self, artists, filename="artist_lyrics", overwrite=False):
        """Save lyrics from multiple Artist objects as JSON object
        :param artists: List of Artist objects to save lyrics from
        :param filename: Name of output file (json)
        :param overwrite: Overwrites preexisting file if True
        """

        # Create a temporary directory for lyrics
        start = time.time()
        tmp_dir = 'tmp_lyrics'
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
            tmp_count = 0
        else:
            tmp_count = len(os.listdir('./' + tmp_dir))

        # Check if file already exists
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
                tmp_file = "." + os.sep + tmp_dir + os.sep + "tmp_{num}_{name}".format(num=(n + tmp_count),
                                                                                       name=artist.name.replace(" ", ""))
                print(tmp_file)
                all_lyrics['artists'][-1] = artist.save_lyrics(filename=tmp_file,
                                                               overwrite=True)
            else:
                warn("Item #{} was not of type Artist. Skipping.".format(n))

        # Save all of the lyrics
        with open(filename + '.json', 'w') as outfile:
            json.dump(all_lyrics, outfile)

        # Delete the temporary directory
        shutil.rmtree(tmp_dir)

        end = time.time()
        print("Time elapsed: {} hours".format((end-start)/60.0/60.0))
