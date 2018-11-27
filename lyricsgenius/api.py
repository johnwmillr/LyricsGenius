# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

"""
API documentation: https://docs.genius.com/
"""

import os
import re
import requests
from requests.exceptions import Timeout
import shutil
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
        response = None
        try:
            response = self._session.request(method, uri,
                                            timeout=self.timeout,
                                            params=params_)

        except Timeout as e:
            print("Timeout raised and caught:\n{e}".format(e=e))

        # Enforce rate limiting
        time.sleep(self.sleep_time)
        return response.json()['response'] if response else None

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
                 skip_non_songs=True, excluded_terms=[],
                 replace_default_terms=False):
        """ Genius Client Constructor

        :param verbose: Turn printed messages on or off (bool)
        :param remove_section_headers: If True, removes [Chorus], [Bridge], etc. headers from lyrics
        :param skip_non_songs: If True, attempts to skip non-songs (e.g. track listings)
        :param excluded_terms: (list) extra terms for flagging results as non-lyrics
        :param replace_default_terms: if True, replaces default excluded terms with user's
        """

        super().__init__(client_access_token, response_format, timeout, sleep_time)
        self.verbose = verbose
        self.remove_section_headers = remove_section_headers
        self.skip_non_songs = skip_non_songs
        self.excluded_terms = excluded_terms
        self.replace_default_terms = replace_default_terms

    def _scrape_song_lyrics_from_url(self, url):
        """ Use BeautifulSoup to scrape song info off of a Genius song URL
        :param url: URL for the web page to scrape lyrics from
        """
        page = requests.get(url)
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
        """ Returns a lowercase string with punctuation and bad chars removed
        :param s: string to clean
        """
        return s.translate(str.maketrans('', '', punctuation)).replace('\u200b', " ").strip().lower()

    def _result_is_lyrics(self, song_title):
        """ Returns False if result from Genius is not actually song lyrics
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
        return not regex.search(self._clean_str(song_title))

    def resultIsAMatch(self, result, title, artist=None):
        """ Returns True if search result matches searched song """
        result_title = self._clean_str(result['title'])
        title_is_match = result_title == self._clean_str(title)
        if not artist:
            return title_is_match
        result_artist = self._clean_str(result['primary_artist']['name'])
        return title_is_match and result_artist == self._clean_str(artist)

    def search_song(self, title, artist="",
                    get_full_info=True, take_first_result=False):
        """ Search Genius.com for lyrics to a specific song
        :param title: Song title to search for
        :param artist: Name of the artist
        :param get_full_info: Get full info for each song (slower)
        :param take_first_result: Force search to choose first result
        """

        # Search the Genius API for the specified song
        if self.verbose:
            if artist:
                print('Searching for "{s}" by {a}...'.format(s=title, a=artist))
            else:
                print('Searching for "{s}"...'.format(s=title))
        search_term = "{s} {a}".format(s=title, a=artist).strip()
        response = self.search_genius(search_term)

        # Exit search if there were no results returned from API
        if (response is None) or (len(response['hits']) == 0):
            if self.verbose:
                print("No results found for: '{s}'".format(s=search_term))
            return None

        # Always take first search result if user didn't specify an artist
        take_first_result = True if artist == "" else take_first_result

        # Loop through the API search results, looking for desired song
        results = [r['result'] for r in response['hits'] if r['type'] == 'song']
        for result in results:
            # Skip to next search result if current result is not a match
            if not (take_first_result or self.resultIsAMatch(result, title, artist)):
                continue

            # Reject non-songs (Liner notes, track lists, etc.)
            if self.skip_non_songs:
                song_is_valid = self._result_is_lyrics(result['title'])
            else:
                song_is_valid = True
            if not song_is_valid:
                if self.verbose:
                    print('Specified song does not contain lyrics. Rejecting.')
                return None

            # Download full song info (an API call) unless told not to by user
            if get_full_info:
                song_info = self.get_song(result['id'])['song']
            else:
                song_info = result
            lyrics = self._scrape_song_lyrics_from_url(song_info['url'])

            # Skip results when URL is a 404 or lyrics are missing
            if not lyrics:
                if self.verbose:
                    print('Specified song does not have a valid URL with lyrics. Rejecting.')
                return None

            # Return a Song object with lyrics if we've made it this far
            song = Song(song_info, lyrics)
            if self.verbose:
                print('Done.')
            return song

        if self.verbose:
            print("Could not find specified song.")
        return None

    def search_artist(self, artist_name, max_songs=None,
                      get_full_info=True, take_first_result=False):
        """Search Genius.com for songs by the specified artist.
        Returns an Artist object containing artist's songs.
        :param artist_name: Name of the artist to search for
        :param max_songs: Maximum number of songs to search for
        :param get_full_info: Get full info for each song (slower)
        :param take_first_result: Force search to choose first result
        """

        if self.verbose:
            print('Searching for songs by {0}...\n'.format(artist_name))

        # Perform a Genius API search for the artist
        response = self.search_genius(artist_name)
        # results = [r['result'] for r in response['hits'] if r['type'] == 'song']
        # # Loop through the API search results, searching for songs by artist
        # for result in results:

        first_result, artist_id = None, None
        for hit in response['hits']:
            found_artist = hit['result']['primary_artist']
            if first_result is None:
                first_result = found_artist
            artist_id = found_artist['id']
            if (take_first_result or
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
            artist_response = self.get_artist_songs(artist_id)

            # Download each song by artist, store as Song objects in Artist object
            keep_searching = True
            next_page, n = 0, 0
            while keep_searching:
                for song_info in artist_response['songs']:
                    # TODO: Shouldn't I use self.search_song() here?

                    # Songs must have a title
                    if 'title' not in song_info:
                        song_info['title'] = 'MISSING TITLE'

                    # Remove non-song results (e.g. Linear Notes, Tracklists, etc.)
                    lyrics = self._scrape_song_lyrics_from_url(song_info['url'])
                    song_is_valid = self._result_is_lyrics(song_info['title']) if (lyrics and self.skip_non_songs) else True

                    if song_is_valid:
                        if get_full_info:
                            song = Song(self.get_song(song_info['id']), lyrics)
                        else:  # Create song with less info (faster)
                            song = Song({'song': song_info}, lyrics)

                        # Add song to the Artist object
                        if artist.add_song(song, verbose=False) == 0:
                            n += 1
                            if self.verbose:
                                print('Song {0}: "{1}"'.format(n, song.title))

                    else:  # Song does not contain lyrics
                        if self.verbose:
                            print('"{title}" does not contain lyrics. Rejecting.'.format(title=song_info['title']))

                    # Check if user specified a max number of songs
                    if not isinstance(max_songs, type(None)):
                        if artist.num_songs >= max_songs:
                            keep_searching = False
                            if self.verbose:
                                print('\nReached user-specified song limit ({0}).'.format(max_songs))
                            break

                # Move on to next page of search results
                next_page = artist_response['next_page']
                if next_page is None:
                    break
                else:  # Get next page of artist song results
                    artist_response = self.get_artist_songs(artist_id, page=next_page)

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
