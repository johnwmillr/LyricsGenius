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
from urllib.parse import urlencode
import shutil
import json
from bs4 import BeautifulSoup
from string import punctuation
import time

from .song import Song
from .artist import Artist


class API(object):
    """Genius API"""

    # Create a persistent requests connection
    _session = requests.Session()
    _session.headers = {'application': 'LyricsGenius',
       'User-Agent': 'https://github.com/johnwmillr/LyricsGenius'}
    _SLEEP_MIN = 0.2  # Enforce minimum wait time between API calls (seconds)

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
        time.sleep(max(self._SLEEP_MIN, self.sleep_time))
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

    def search_genius_web(self, search_term, per_page=5):
        """Use the web-version of Genius search"""
        endpoint = "search/multi?"
        params = {'per_page': per_page, 'q': search_term}

        # This endpoint is not part of the API, requires different formatting
        url = "https://genius.com/api/" + endpoint + urlencode(params)
        response = requests.get(url)
        time.sleep(max(self._SLEEP_MIN, self.sleep_time))
        return response.json()['response'] if response else None

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
            print("Could not find specified song. Check spelling?")
        return None

    def search_artist(self, artist_name, max_songs=None, sort='title',
                      per_page=20, get_full_info=True,
                      take_first_result=False):
        """Search Genius.com for songs by the specified artist.
        Returns an Artist object containing artist's songs.
        :param artist_name: Name of the artist to search for
        :param max_songs: Maximum number of songs to search for
        :param sort: Sort by 'title' or 'popularity'
        :param per_page: Number of results to return per search page
        :param get_full_info: Get full info for each song (slower)
        :param take_first_result: Force search to choose first result
        """

        if self.verbose:
            print('Searching for songs by {0}...\n'.format(artist_name))

        # Perform a Genius API search for the artist
        response = self.search_genius_web(artist_name)
        hits = response['sections'][0]['hits']
        top_artists = [hit for hit in hits if hit['type'] == 'artist']

        # Exit the search if we couldn't find an artist by the given name
        if not len(top_artists):
            if self.verbose:
                print("No results found for '{a}'.".format(a=artist_name))
            return None

        # Assume the top search result is the intended artist
        found_artist = top_artists[0]['result']
        artist_id = found_artist['id']
        artist_info = self.get_artist(artist_id)
        found_name = artist_info['artist']['name']
        if found_name != artist_name:
            if self.verbose:
                print("Changing artist name to '{a}'".format(a=found_name))
            artist_name = found_name

        # Create the Artist object
        artist = Artist(artist_info)

        # Download each song by artist, stored as Song objects in Artist object
        page = 1
        reached_max_songs = False
        while not reached_max_songs:
            songs_on_page = self.get_artist_songs(artist_id, sort, per_page, page)

            # Loop through each song on page of search results
            for song_info in songs_on_page['songs']:
                # Check if song is valid (e.g. has title, contains lyrics)
                has_title = ('title' in song_info)
                has_lyrics = self._result_is_lyrics(song_info['title'])
                song_is_valid = has_title and (has_lyrics or (not self.skip_non_songs))

                # Reject non-song results (e.g. Linear Notes, Tracklists, etc.)
                if not song_is_valid:
                    if self.verbose:
                        s = song_info['title'] if has_title else "MISSING TITLE"
                        print('"{s}" is not valid. Skipping.'.format(s=s))
                    continue

                # Create the Song object from lyrics and metadata
                lyrics = self._scrape_song_lyrics_from_url(song_info['url'])
                if get_full_info:
                    info = self.get_song(song_info['id'])
                else:
                    info = {'song': song_info}
                song = Song(info, lyrics)

                # Attempt to add the Song to the Artist
                result = artist.add_song(song, verbose=False)
                if result == 0 and self.verbose:
                    print('Song {n}: "{t}"'.format(n=artist.num_songs,
                                                   t=song.title))

                # Exit search if the max number of songs has been met
                reached_max_songs = max_songs and artist.num_songs >= max_songs
                if reached_max_songs:
                    if self.verbose:
                        print('\nReached user-specified song limit ({m}).'.format(m=max_songs))
                    break

            # Move on to next page of search results
            page = songs_on_page['next_page']
            if page is None:
                break  # Exit search when last page is reached

        if self.verbose:
            print('Done. Found {n} songs.'.format(n=artist.num_songs))
        return artist

    def save_artists(self, artists, filename="artist_lyrics", overwrite=False):
        """Save lyrics from multiple Artist objects as JSON object
        :param artists: List of Artist objects to save lyrics from
        :param filename: Name of output file (json)
        :param overwrite: Overwrites preexisting file if True
        """
        if isinstance(artists, Artist):
            artists = [artists]

        # Create a temporary directory for lyrics
        start = time.time()
        tmp_dir = 'tmp_lyrics'
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
            count = 0
        else:
            count = len(os.listdir(tmp_dir))

        # Check if file already exists
        if os.path.isfile(filename + ".json") and not overwrite:
            msg = "{f} already exists. Overwrite?\n(y/n): ".format(f=filename)
            if input(msg).lower() != "y":
                print("Leaving file in place. Exiting.")
                os.rmdir(tmp_dir)
                return

        # Extract each artist's lyrics in json format
        all_lyrics = {'artists': []}
        for n, artist in enumerate(artists):
            if isinstance(artist, Artist):
                all_lyrics['artists'].append({})
                f = "tmp_{n}_{a}".format(n=count + n,
                                         a=artist.name.replace(" ", ""))
                tmp_file = os.path.join(tmp_dir, f)
                if self.verbose:
                    print(tmp_file)
                all_lyrics['artists'][-1] = artist.save_lyrics(filename=tmp_file,
                                                               overwrite=True)

        # Save all of the lyrics
        with open(filename + '.json', 'w') as outfile:
            json.dump(all_lyrics, outfile)

        # Delete the temporary directory
        shutil.rmtree(tmp_dir)
        elapsed = (time.time() - start) / 60 / 60
        print("Time elapsed: {t} hours".format(t=elapsed))
