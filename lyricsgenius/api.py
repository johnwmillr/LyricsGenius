# GeniusAPI
# John W. Miller
# See LICENSE for details

"""API documentation: https://docs.genius.com/"""

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

from lyricsgenius.song import Song
from lyricsgenius.artist import Artist


class API(object):
    """Genius API.
    The :obj:`API` class is in charge of making all the requests
    to the developers' API, and the public API.
    Use the methods of this class if you already have information
    such as song ID to make direct requests to the API. Otherwise
    the :class:`Genius` class provides a friendlier front-end
    to search and retrieve data from Genius.com.

    | All methods of this class are available through the :class:`Genius` class.

    Args:
        client_access_token (:obj:`str`): API key provided by Genius.
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.

    Attributes:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.

    Returns:
        :class:`API`: An object of the `API` class.

    """

    # Create a persistent requests connection
    _session = requests.Session()
    _session.headers = {'application': 'LyricsGenius',
                        'User-Agent': 'https://github.com/johnwmillr/LyricsGenius'}
    _SLEEP_MIN = 0.2  # Enforce minimum wait time between API calls (seconds)

    def __init__(self, client_access_token,
                 response_format='plain', timeout=5, sleep_time=0.5):
        # Genius API Constructor

        self._ACCESS_TOKEN = client_access_token
        self._session.headers['authorization'] = 'Bearer ' + self._ACCESS_TOKEN
        self.response_format = response_format.lower()
        self.api_root = 'https://api.genius.com/'
        self.timeout = timeout
        self.sleep_time = sleep_time

    def _make_request(self, path, method='GET', params_=None):
        """Makes a request to the API."""
        uri = self.api_root + path

        params_ = params_ if params_ else {}
        params_['text_format'] = self.response_format

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
        """Gets data for a specific song.

        Args:
            id\\_ (:obj:`int`): Genius song ID

        Returns:
            :obj:`dict`: Song details from Genius.

        Examples:
            .. code:: python

                genius = Genius(token)
                song = genius.get_song(2857381)
                print(song['full_title'])

        Note:
            This pure API method is used for fetching songs when you have their ID,
            and only makes a request to the API, therefore provides no lyrics.
            If you want the lyrics as well, use :meth:`Genius.search_song` instead.

        """
        endpoint = "songs/{id}".format(id=id_)
        return self._make_request(endpoint)

    def get_artist(self, id_):
        """Gets data for a specific artist.

        Args:
            id_ (:obj:`int`): Genius artist ID

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                genius = Genius(token)
                artist = genius.get_artist(380491)
                print(artist['name'])

        """
        endpoint = "artists/{id}".format(id=id_)
        return self._make_request(endpoint)

    def get_artist_songs(self, id_, sort='title', per_page=20, page=1):
        """Documents (songs) for the artist specified.

        Args:
            id_ (:obj:`int`): Genius artist ID
            sort (:obj:`str`, optional): Sorting preference.
                Either based on 'title' or 'popularity'.
            per_page (:obj:`str`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                # getting all artist songs based on popularity
                genius = Genius(token)
                page = 1
                songs = []
                while page:
                    request = genius.get_artist_songs(380491,
                                                        sort='popularity',
                                                        per_page=50,
                                                        page=page)
                songs.extend(request['songs'])
                page = request['next_page']
                least_popular_song = songs[-1]['title']


                # getting songs 11-15
                songs = genius.get_artist_songs(380491, per_page=5, page=3)

        """
        endpoint = "artists/{id}/songs".format(id=id_)
        params = {'sort': sort, 'per_page': per_page, 'page': page}
        return self._make_request(endpoint, params_=params)

    def get_referents(self, song_id=None, web_page_id=None,
                      created_by_id=None, per_page=20, page=1):
        """Gets song's referents

        Args:
            song_id (:obj:`int`, optional): song ID
            web_page_id (:obj:`int`, optional): web page ID
            created_by_id (:obj:`int`, optional): User ID of the contributer
                who created the annotation(s).
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 50.

        Returns:
            :obj:`dict`

        Note:
            You may pass only one of :obj:`song_id` and
            :obj:`web_page_id`, not both.

        Examples:
            .. code:: python

                # getting all verified annotations of a song (artist annotations)
                genius = Genius(token)
                request = genius.get_referents(song_id=235729,
                                                per_page=50)
                verified = [y for x in request['referents']
                            for y in x['annotations'] if y['verified']]
        """
        msg = "Must supply `song_id`, `web_page_id`, or `created_by_id`."
        assert any([song_id, web_page_id, created_by_id]), msg
        if song_id or web_page_id:
            msg = "Pass only one of `song_id` and `web_page_id`, not both."
            assert bool(song_id) ^ bool(web_page_id), msg

        # Construct the URI
        endpoint = "referents?"
        params = {'song_id': song_id, 'web_page_id': web_page_id,
                  'created_by_id': created_by_id,
                  'per_page': per_page, 'page': page}
        return self._make_request(endpoint, params_=params)

    def get_annotation(self, id_):
        """Gets data for a specific annotation.

        Args:
            id_ (:obj:`int`): annotation ID

        Returns:
            :obj:`dict`

        """
        endpoint = "annotations/{id}".format(id=id_)
        return self._make_request(endpoint)

    def get_song_annotations(self, song_id):
        """Return song's annotations with associated fragment in list of tuple.

        Args:
            song_id (:obj:`int`): song ID

        Returns:
            :obj:`list`: list of tuples(fragment, [annotations])

        Note:
            This method uses :meth:`Genius.get_referents`, but provides convenient
            access to fragments (annotated text) and the corresponding
            annotations (Some fragments may have more than one annotation,
            because sometimes both artists and Genius users annotate them).

        """
        referents = self.get_referents(song_id=song_id)["referents"]
        all_annotations = []  # list of tuples(fragment, annotations[])
        for r in referents:
            fragment = r["fragment"]
            annotations = []
            for a in r["annotations"]:
                annotations.append(a["body"]["plain"])
            all_annotations.append((fragment, annotations))
        return all_annotations

    def search_genius(self, search_term):
        """Searches documents hosted on Genius.

        Regardless of the :obj:`search_term` this method
        only returns songs.

        Args:
            search_term (:obj:`str`): A term to search on Genius

        Returns:
            :obj:`dict`

        """
        endpoint = "search/"
        params = {'q': search_term}
        return self._make_request(endpoint, params_=params)

    def search_genius_web(self, search_term, per_page=5):
        """Uses the web-version of Genius search.
        This method makes a request to the public API.

        Args:
            search_term (:obj:`str`): A term to search on Genius.
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 50.

        Returns:
            :obj:`dict` \\| :obj:`None`: If there is a response, otherwise `None`.

        Tip:
            This method returns various sections including: :obj:`top_hit`,
            :obj:`song`, :obj:`lyric`, :obj:`album`, :obj:`video`,
            :obj:`article`, :obj:`user`.

            This method is especially useful for searching Genius and
            accessing the top results of each section e.g. searching
            for a song by lyrics.

        Examples:
            .. code:: python

                # looking at the type of the top hits
                genius = Genius(token)
                request = genius.search_genius_web('Andy Shauf The Party')
                for hit in request['sections'][0]['hits']:
                    print(hit['type'])

        """
        endpoint = "search/multi?"
        params = {'per_page': per_page, 'q': search_term}

        # This endpoint is not part of the API, requires different formatting
        url = "https://genius.com/api/" + endpoint + urlencode(params)
        response = requests.get(url, timeout=self.timeout)
        time.sleep(max(self._SLEEP_MIN, self.sleep_time))
        return response.json()['response'] if response else None


class Genius(API):
    """User-level interface with the Genius.com API.

    Args:
        client_access_token (:obj:`str`): API key provided by Genius.
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.
        verbose (:obj:`bool`, optional): Turn printed messages on or off.
        remove_section_headers (:obj:`bool`, optional): If `True`, removes [Chorus],
            [Bridge], etc. headers from lyrics.
        skip_non_songs (:obj:`bool`, optional): If `True`, attempts to
            skip non-songs (e.g. track listings).
        excluded_terms (:obj:`list`, optional): extra terms for flagging results
            as non-lyrics.
        replace_default_terms (:obj:`list`, optional): if True, replaces default
            excluded terms with user's. Default excluded terms are listed below.

    Attributes:
        verbose (:obj:`bool`, optional): Turn printed messages on or off.
        remove_section_headers (:obj:`bool`, optional): If `True`, removes [Chorus],
            [Bridge], etc. headers from lyrics.
        skip_non_songs (:obj:`bool`, optional): If `True`, attempts to
            skip non-songs (e.g. track listings).
        excluded_terms (:obj:`list`, optional): extra terms for flagging results
            as non-lyrics.
        replace_default_terms (:obj:`list`, optional): if True, replaces default
            excluded terms with user's.

    Returns:
        :class:`Genius`

    Note:
        Default excluded terms are the following regular expressions:
        :obj:`track\\s?list`, :obj:`album art(work)?`, :obj:`liner notes`,
        :obj:`booklet`, :obj:`credits`, :obj:`interview`, :obj:`skit`,
        :obj:`instrumental`, and :obj:`setlist`.

    """

    def __init__(self, client_access_token,
                 response_format='plain', timeout=5, sleep_time=0.5,
                 verbose=True, remove_section_headers=False,
                 skip_non_songs=True, excluded_terms=None,
                 replace_default_terms=False):
        # Genius Client Constructor

        super().__init__(client_access_token, response_format, timeout, sleep_time)
        self.verbose = verbose
        self.remove_section_headers = remove_section_headers
        self.skip_non_songs = skip_non_songs
        self.excluded_terms = excluded_terms
        self.replace_default_terms = replace_default_terms

    def _scrape_song_lyrics_from_url(self, url):
        """Uses BeautifulSoup to scrape song info off of a Genius song URL

        Args:
            url (:obj:`str`, optional): URL for the web page to scrape lyrics from.

        Returns:
            :obj:`str` \\|‌ :obj:`None`: If it can find the lyrics, otherwise `None`

        Note:
            This method removes the song headers based on the value of the
            :attr:`remove_section_headers` attribute.

        """
        page = requests.get(url)
        if page.status_code == 404:
            if self.verbose:
                print("Song URL returned 404.")
            return None

        # Scrape the song lyrics from the HTML
        html = BeautifulSoup(page.text, "html.parser")

        # Determine the class of the div
        old_div = html.find("div", class_="lyrics")
        if old_div:
            lyrics = old_div.get_text()
        else:
            new_div = html.find("div", class_=re.compile("Lyrics__Root"))
            if new_div:
                lyrics = new_div.get_text('\n').replace('\n[', '\n\n[')
            else:
                if self.verbose:
                    print("Couldn't find the lyrics section.")
                return None

        if self.remove_section_headers:  # Remove [Verse], [Bridge], etc.
            lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
            lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
        return lyrics.strip("\n")

    def _clean_str(self, s):
        """Returns a lowercase string with punctuation and bad chars removed."""
        return (s.translate(str.maketrans('', '', punctuation))
                .replace('\u200b', " ").strip().lower())

    def _result_is_lyrics(self, song_title):
        """Returns False if result from Genius is not actually song lyrics.

        Sets the :attr:`lyricsgenius.Genius.excluded_terms` and
        :attr:`lyricsgenius.Genius.replace_default_terms` as instance variables
        within the Genius class.

        Args:
            song_title (:obj:`str`, optional): Title of the song.

        Returns:
            :obj:`bool`: `True` if none of the terms are found in the song title.

        Note:
            Default excluded terms are the following: 'track\\s?list',
            'album art(work)?', 'liner notes', 'booklet', 'credits',
            'interview', 'skit', 'instrumental', and 'setlist'.

        """

        default_terms = ['track\\s?list', 'album art(work)?', 'liner notes',
                         'booklet', 'credits', 'interview', 'skit',
                         'instrumental', 'setlist']
        if self.excluded_terms:
            if self.replace_default_terms:
                default_terms = self.excluded_terms
            else:
                default_terms.extend(self.excluded_terms)

        expression = r"".join(["({})|".format(term) for term in default_terms])
        expression = expression.strip('|')
        regex = re.compile(expression, re.IGNORECASE)
        return not regex.search(self._clean_str(song_title))

    def _get_item_from_search_response(self, response, search_term, type_, result_type):
        """Returns either a :class:`lyricsgenius.Song` or
        :class:`lyricsgenius.artist.Artist` result from
        :meth:`Genius.search_genius_web`.

        This method tries to match the `hits` of the :obj:`response` to
            the :obj:`response_term`, and if it finds no match, returns the first hit
            if there are any.

        Args:
            response (:obj:`dict`): A response from
                :meth:‍‍‍‍`Genius.search_genius_web` to go through.
            search_term (:obj:`str`): The search term to match with the hit.
            type_ (:obj:`str`): Type of the hit we're looking for (e.g. song, artist).
            result_type (:obj:`str`): The part of the hit we want to match
                (e.g. song title, artist's name).

        Returns:
            :obj:‍‍`str` \\|‌ :obj:`None`:
            - `None` if there is no hit in the :obj:`response`.
            - The matched result if matching succeeds.
            - The first hit if the matching fails.

        """

        # Convert list to dictionary
        hits = response['sections'][0]['hits']

        # Check rest of results if top hit wasn't the search type
        sections = sorted(response['sections'],
                          key=lambda sect: sect['type'] == type_,
                          reverse=True)

        hits = [hit for section in sections
                for hit in section['hits']
                if hit['type'] == type_]

        for hit in hits:
            if hit['result'][result_type] == search_term:
                return hit['result']

        return hits[0]['result'] if hits else None

    def _result_is_match(self, result, title, artist=None):
        """Returns `True` if search result matches searched song."""
        result_title = self._clean_str(result['title'])
        title_is_match = result_title == self._clean_str(title)
        if not artist:
            return title_is_match
        result_artist = self._clean_str(result['primary_artist']['name'])
        return title_is_match and result_artist == self._clean_str(artist)

    def search_song(self, title, artist="", get_full_info=True):
        """Searches Genius.com for the lyrics to a specific song.

        Args:
            title (:obj:`str`): Song title to search for.
            artist (:obj:`str`, optional): Name of the artist.
            get_full_info (:obj:`bool`, optional): Get full info for each song (slower).

        Returns:
            :class:`Song <lyricsgenius.song.Song>` \\| :obj:`None`: On success,
            the song object is returned, otherwise `None`.

        Tip:
            Set :attr:`Genius.verbose` to `True` to read why the search fails.

        Examples:
            .. code:: python

                genius = Genius(token)
                artist = genius.search_artist('Andy Shauf', max_songs=0)
                song = genius.search_song('Toy You', artist.name)
                # same as: song = genius.search_song('To You', 'Andy Shauf')
                print(song['lyrics'])

        """
        if self.verbose:
            if artist:
                print('Searching for "{s}" by {a}...'.format(s=title, a=artist))
            else:
                print('Searching for "{s}"...'.format(s=title))
        search_term = "{s} {a}".format(s=title, a=artist).strip()
        response = self.search_genius_web(search_term)

        # Otherwise, move forward with processing the search results
        result = self._get_item_from_search_response(response, title, type_="song",
                                                     result_type="title")

        # Exit search if there were no results returned from API
        if not result:
            if self.verbose:
                print("No results found for: '{s}'".format(s=search_term))
            return None

        # Reject non-songs (Liner notes, track lists, etc.)
        valid = self._result_is_lyrics(result['title']) if self.skip_non_songs else True
        if not valid:
            if self.verbose:
                print('Specified song does not contain lyrics. Rejecting.')
            return None

        # Download full song info (an API call) unless told not to by user
        song_info = result.copy()
        if get_full_info:
            song_info.update(self.get_song(result['id'])['song'])
        lyrics = self._scrape_song_lyrics_from_url(song_info['url'])

        # Skip results when URL is a 404 or lyrics are missing
        if not lyrics:
            if self.verbose:
                print(('Specified song does not have a valid URL with lyrics.'
                       'Rejecting.'))
            return None

        # Return a Song object with lyrics if we've made it this far
        song = Song(song_info, lyrics)
        if self.verbose:
            print('Done.')
        return song

    def search_artist(self, artist_name, max_songs=None,
                      sort='popularity', per_page=20,
                      get_full_info=True,
                      allow_name_change=True,
                      artist_id=None,
                      include_features=False):
        """Searches Genius.com for songs by the specified artist.
        This method looks for the artist by the name or by the
        ID if it's provided. It returrns an :class:`Artist <lyricsgenius.artist.Artist>`
        object if the search is successful.
        If :obj:`allow_name_change` is True, the name of the artist is changed to the
        artist name on Genius.

        Args:
            artist_name (:obj:`str`): Name of the artist to search for.
            max_songs (obj:`int`, optional): Maximum number of songs to search for.
            sort (:obj:`str`, optional): Sort by 'title' or 'popularity'.
            per_page (:obj:`int`, optional): Number of results to return
                per search page. It can't be more than 50.
            get_full_info (:obj:`bool`, optional): Get full info for each song (slower).
            allow_name_change (:obj:`bool`, optional): If True, search attempts to
                switch to intended artist name.
            artist_id (:obj:`int`, optional): Allows user to pass an artist ID.
            include_features (:obj:`bool`, optional): If True, includes tracks
                featuring the artist.

        Returns:
            :class:`Artist <lyricsgenius.artist.Artist>`: Artist object containing
            artist's songs.

        Examples:
            .. code:: python

                # printing the lyrics of all of the artist's songs
                genius = Genius(token)
                artist = genius.search_artist('Andy Shauf')
                for song in artist.songs:
                    print(song.lyrics)

            Visit :class:`Aritst <lyricsgenius.artist.Artist>` for more examples.
        """
        def find_artist_id(search_term):
            """Finds the ID of the artist, returns the first
            result if none match the search term or returns
            ‍None‍‍ if there were not results

            """
            if self.verbose:
                print('Searching for songs by {0}...\n'.format(search_term))

            # Perform a Genius API search for the artist
            found_artist = None
            response = self.search_genius_web(search_term)
            found_artist = self._get_item_from_search_response(response,
                                                               search_term,
                                                               type_="artist",
                                                               result_type="name")

            # Exit the search if we couldn't find an artist by the given name
            if not found_artist:
                if self.verbose:
                    print("No results found for '{a}'.".format(a=search_term))
                return None
            # Assume the top search result is the intended artist
            return found_artist['id']

        # Get the artist ID (or use the one supplied)
        artist_id = artist_id if artist_id else find_artist_id(artist_name)
        if not artist_id:
            return None

        artist_info = self.get_artist(artist_id)
        found_name = artist_info['artist']['name']
        if found_name != artist_name and allow_name_change:
            if self.verbose:
                print("Changing artist name to '{a}'".format(a=found_name))
            artist_name = found_name

        # Create the Artist object
        artist = Artist(artist_info)
        # Download each song by artist, stored as Song objects in Artist object
        page = 1
        reached_max_songs = True if max_songs == 0 else False
        while not reached_max_songs:
            songs_on_page = self.get_artist_songs(artist_id, sort, per_page, page)

            # Loop through each song on page of search results
            for song_info in songs_on_page['songs']:
                # Check if song is valid (e.g. has title, contains lyrics)
                has_title = ('title' in song_info)
                has_lyrics = self._result_is_lyrics(song_info['title'])
                valid = has_title and (has_lyrics or (not self.skip_non_songs))

                # Reject non-song results (e.g. Linear Notes, Tracklists, etc.)
                if not valid:
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
                result = artist.add_song(song, verbose=False,
                                         include_features=include_features)
                if result == 0 and self.verbose:
                    print('Song {n}: "{t}"'.format(n=artist.num_songs,
                                                   t=song.title))

                # Exit search if the max number of songs has been met
                reached_max_songs = max_songs and artist.num_songs >= max_songs
                if reached_max_songs:
                    if self.verbose:
                        print(('\nReached user-specified song limit ({m}).'
                               .format(m=max_songs)))
                    break

            # Move on to next page of search results
            page = songs_on_page['next_page']
            if page is None:
                break  # Exit search when last page is reached

        if self.verbose:
            print('Done. Found {n} songs.'.format(n=artist.num_songs))
        return artist

    def save_artists(self, artists, filename="artist_lyrics", overwrite=False):
        """Saves lyrics from multiple Artist objects as JSON object.

        Args:
            artists (:obj:`list`): List of :class:`Artist <lyricsgenius.artist.Artist>`
                objects to save lyrics from.
            filename (:obj:`str`, optional): Name of the output file.
            overwrite (:obj:`bool`, optional): Overwrites preexisting file if `True`.
                Otherwise prompts user for input.

        Examples:
            .. code:: python

                genius = Genius(token)
                a = search_artist('Andy Shauf')
                b = search_artist('Queen', max_song=10)
                c = search_artist('The Beatles', max_songs=1)

                genius.save_artists(artists=[a, b, c], filename='abc', overwrite=True)

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
                all_lyrics['artists'][-1] = artist.save_lyrics(overwrite=True)

        # Save all of the lyrics
        with open(filename + '.json', 'w') as outfile:
            json.dump(all_lyrics, outfile)

        # Delete the temporary directory
        shutil.rmtree(tmp_dir)
        elapsed = (time.time() - start) / 60 / 60
        print("Time elapsed: {t} hours".format(t=elapsed))
