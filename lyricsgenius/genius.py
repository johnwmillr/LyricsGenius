# GeniusAPI
# John W. Miller
# See LICENSE for details

"""API documentation: https://docs.genius.com/"""

import os
import re
import shutil
import json
import time
from string import punctuation

import requests
from bs4 import BeautifulSoup

from .types import Album, Artist, Song
from .api import API, PublicAPI


class Genius(API, PublicAPI):
    """User-level interface with the Genius.com API and public API.

    Args:
        access_token (:obj:`str`, optional): API key provided by Genius.
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
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

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
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

    Returns:
        :class:`Genius`

    Note:
        Default excluded terms are the following regular expressions:
        :obj:`track\\s?list`, :obj:`album art(work)?`, :obj:`liner notes`,
        :obj:`booklet`, :obj:`credits`, :obj:`interview`, :obj:`skit`,
        :obj:`instrumental`, and :obj:`setlist`.

    """

    def __init__(self, access_token=None,
                 response_format='plain', timeout=5, sleep_time=0.5,
                 verbose=True, remove_section_headers=False,
                 skip_non_songs=True, excluded_terms=None,
                 replace_default_terms=False,
                 retries=0,
                 ):
        # Genius Client Constructor
        super().__init__(
            access_token=access_token,
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time,
            retries=retries
        )

        self.verbose = verbose
        self.remove_section_headers = remove_section_headers
        self.skip_non_songs = skip_non_songs
        self.excluded_terms = excluded_terms
        self.replace_default_terms = replace_default_terms

    def lyrics(self, urlthing, remove_section_headers=False):
        """Uses BeautifulSoup to scrape song info off of a Genius song URL

        Args:
            urlthing (:obj:`str` | :obj:`int`):
                Song ID or song URL.
            remove_section_headers (:obj:`bool`, optional):
                If `True`, removes [Chorus], [Bridge], etc. headers from lyrics.

        Returns:
            :obj:`str` \\|‌ :obj:`None`:
                :obj:`str` If it can find the lyrics, otherwise `None`

        Note:
            If you pass a song ID, the method will have to make an extra request
            to obtain the song's URL and scrape the lyrics off of it. So it's best
            to pass the method the song's URL if its available.

            If you want to get a song's lyrics by searching for it,
            use :meth:`Genius.search_song` instead.

        Note:
            This method removes the song headers based on the value of the
            :attr:`Genius.remove_section_headers` attribute.

        """
        if isinstance(urlthing, int):
            url = self.song(urlthing)['song']['url']
        else:
            url = urlthing

        if not url.startswith("https://genius.com/"):
            if self.verbose:
                print("Song URL is not valid.")
            return None

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
                    print("Couldn't find the lyrics section. "
                          "Please report this if the song has lyrics.\n"
                          "Song URL: {}".format(url))
                return None

        # Remove [Verse], [Bridge], etc.
        if self.remove_section_headers or remove_section_headers:
            lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
            lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
        return lyrics.strip("\n")

    def _clean_str(self, s):
        """Returns a lowercase string with punctuation and bad chars removed."""
        punctuation_ = punctuation + "’"
        return (s.translate(str.maketrans('', '', punctuation_))
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
        """Gets the desired item from the search results.

        This method tries to match the `hits` of the :obj:`response` to
        the :obj:`response_term`, and if it finds no match, returns the first
        appropriate hit if there are any.

        Args:
            response (:obj:`dict`): A response from
                :meth:‍‍‍‍`Genius.search_all` to go through.
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
        top_hits = response['sections'][0]['hits']

        # Check rest of results if top hit wasn't the search type
        sections = sorted(response['sections'],
                          key=lambda sect: sect['type'] == type_)

        hits = [hit for hit in top_hits if hit['type'] == type_]
        hits.extend([hit for section in sections
                     for hit in section['hits']
                     if hit['type'] == type_])

        for hit in hits:
            item = hit['result']
            if self._clean_str(item[result_type]) == self._clean_str(search_term):
                return item

        # If the desired type is song lyrics and none of the results matched,
        # return the first result that has lyrics
        if type_ == 'song' and self.skip_non_songs:
            for hit in hits:
                song = hit['result']
                if self._result_is_lyrics(song['title']):
                    return song

        return hits[0]['result'] if hits else None

    def _result_is_match(self, result, title, artist=None):
        """Returns `True` if search result matches searched song."""
        result_title = self._clean_str(result['title'])
        title_is_match = result_title == self._clean_str(title)
        if not artist:
            return title_is_match
        result_artist = self._clean_str(result['primary_artist']['name'])
        return title_is_match and result_artist == self._clean_str(artist)

    def song_annotations(self, song_id, text_format=None):
        """Return song's annotations with associated fragment in list of tuple.

        Args:
            song_id (:obj:`int`): song ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`list`: list of tuples(fragment, [annotations])

        Note:
            This method uses :meth:`Genius.referents`, but provides convenient
            access to fragments (annotated text) and the corresponding
            annotations (Some fragments may have more than one annotation,
            because sometimes both artists and Genius users annotate them).

        """
        referents = self.referents(song_id=song_id,
                                   text_format=text_format)

        all_annotations = []  # list of tuples(fragment, annotations[])
        for r in referents["referents"]:
            fragment = r["fragment"]
            annotations = []
            for a in r["annotations"]:
                annotations.append([x for x in a["body"].values()])
            all_annotations.append((fragment, annotations))
        return all_annotations

    def search_album(self, name=None, artist="",
                     album_id=None, get_full_info=True, text_format=None):
        """Searches for a specific album and gets its songs.

        You must pass either a :obj:`name` or an :obj:`album_id`.

        Args:
            name (:obj:`str`, optional): Album name to search for.
            artist (:obj:`str`, optional): Name of the artist.
            album_id (:obj:`int`, optional): Album ID.
            get_full_info (:obj:`bool`, optional): Get full info
                for the album (slower if no album_id present).
            text_format (:obj:`bool`, optional): If ``True``,
                gets each song's lyrics.

        Returns:
            :class:`Album <types.Album>` \\| :obj:`None`: On success,
            the album object is returned, otherwise `None`.

        Tip:
            Set :attr:`Genius.verbose` to `True` to read why the search fails.

        Examples:
            .. code:: python

                genius = Genius(token)
                album = genius.search_album("Andy Shauf", "The Party")
                print(album.name)

        """
        msg = "You must pass either a `name` or an `album_id`."
        assert any([name, album_id]), msg

        if self.verbose and name:
            if artist:
                print('Searching for "{s}" by {a}...'.format(s=name, a=artist))
            else:
                print('Searching for "{s}"...'.format(s=name))

        if album_id:
            album_info = self.album(album_id, text_format).get('album')
        else:
            search_term = "{s} {a}".format(s=name, a=artist).strip()
            response = self.search_all(search_term)
            album_info = self._get_item_from_search_response(response, name,
                                                             type_="album",
                                                             result_type="name")

        # Exit search if there were no results returned from API
        # Otherwise, move forward with processing the search results
        if album_info is None:
            if self.verbose and name:
                print("No results found for: '{s}'".format(s=search_term))
            return None

        album_id = album_info['id']

        songs = []
        next_page = 1
        while next_page:
            tracks = self.album_tracks(album_id=album_id,
                                       per_page=50,
                                       page=next_page,
                                       text_format=text_format)
            for track in tracks['tracks']:
                song_info = track['song']
                song_lyrics = self.lyrics(song_info['url'])
                song = Song(self, song_info, song_lyrics)
                songs.append(song)

            next_page = tracks['next_page']

        if album_id is None and get_full_info is True:
            new_info = self.album(album_id, text_format=text_format)['album']
            album_info.update(new_info)

        return Album(self, album_info, songs)

    def search_song(self, title=None, artist="", song_id=None,
                    get_full_info=True):
        """Searches for a specific song and gets its lyrics.

        You must pass either a :obj:`title` or a :obj:`song_id`.

        Args:
            title (:obj:`str`): Song title to search for.
            artist (:obj:`str`, optional): Name of the artist.
            get_full_info (:obj:`bool`, optional): Get full info for each song (slower).
            song_id (:obj:`int`, optional): Song ID.

        Returns:
            :class:`Song <types.Song>` \\| :obj:`None`: On success,
            the song object is returned, otherwise `None`.

        Tip:
            Set :attr:`Genius.verbose` to `True` to read why the search fails.

        Examples:
            .. code:: python

                genius = Genius(token)
                artist = genius.search_artist('Andy Shauf', max_songs=0)
                song = genius.search_song('Toy You', artist.name)
                # same as: song = genius.search_song('To You', 'Andy Shauf')
                print(song.lyrics)

        """
        msg = "You must pass either a `title` or a `song_id`."
        if title is None and song_id is None:
            assert any([title, song_id]), msg

        if self.verbose and title:
            if artist:
                print('Searching for "{s}" by {a}...'.format(s=title, a=artist))
            else:
                print('Searching for "{s}"...'.format(s=title))

        if song_id:
            result = self.song(song_id)['song']
        else:
            search_term = "{s} {a}".format(s=title, a=artist).strip()
            search_response = self.search_all(search_term)
            result = self._get_item_from_search_response(search_response,
                                                         title,
                                                         type_="song",
                                                         result_type="title")

        # Exit search if there were no results returned from API
        # Otherwise, move forward with processing the search results
        if result is None:
            if self.verbose and title:
                print("No results found for: '{s}'".format(s=search_term))
            return None

        # Reject non-songs (Liner notes, track lists, etc.)
        if (self.skip_non_songs
            and (result['lyrics_state'] != 'complete'
                 or not self._result_is_lyrics(result['title'])
                 )):
            valid = False
        else:
            valid = True

        if not valid:
            if self.verbose:
                print('Specified song does not contain lyrics. Rejecting.')
            return None

        song_id = result['id']

        # Download full song info (an API call) unless told not to by user
        song_info = result
        if song_id is None and get_full_info is True:
            new_info = self.song(song_id)['song']
            song_info.update(new_info)
        lyrics = self.lyrics(song_info['url'])

        # Skip results when URL is a 404 or lyrics are missing
        if not lyrics:
            if self.verbose:
                print(('Specified song does not have a valid URL with lyrics.'
                       'Rejecting.'))
            return None

        # Return a Song object with lyrics if we've made it this far
        song = Song(self, song_info, lyrics)
        if self.verbose:
            print('Done.')
        return song

    def search_artist(self, artist_name, max_songs=None,
                      sort='popularity', per_page=20,
                      get_full_info=True,
                      allow_name_change=True,
                      artist_id=None,
                      include_features=False,
                      ):
        """Searches for a specific artist and gets their songs.

        This method looks for the artist by the name or by the
        ID if it's provided in ``artist_id``. It returrns an
        :class:`Artist <types.Artist>` object if the search is successful.
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
            :class:`Artist <types.Artist>`: Artist object containing
            artist's songs.

        Examples:
            .. code:: python

                # printing the lyrics of all of the artist's songs
                genius = Genius(token)
                artist = genius.search_artist('Andy Shauf')
                for song in artist.songs:
                    print(song.lyrics)

            Visit :class:`Aritst <types.Artist>` for more examples.
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
            response = self.search_all(search_term)
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

        artist_info = self.artist(artist_id)['artist']
        found_name = artist_info['name']
        if found_name != artist_name and allow_name_change:
            if self.verbose:
                print("Changing artist name to '{a}'".format(a=found_name))
            artist_name = found_name

        # Create the Artist object
        artist = Artist(self, artist_info)
        # Download each song by artist, stored as Song objects in Artist object
        page = 1
        reached_max_songs = True if max_songs == 0 else False
        while not reached_max_songs:
            songs_on_page = self.artist_songs(artist_id=artist_id,
                                              per_page=per_page,
                                              page=page,
                                              sort=sort,
                                              )

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
                lyrics = self.lyrics(song_info['url'])
                if get_full_info:
                    new_info = self.song(song_info['id'])['song']
                    song_info.update(new_info)
                song = Song(self, song_info, lyrics)

                # Attempt to add the Song to the Artist
                result = artist.add_song(song, verbose=False,
                                         include_features=include_features)
                if result is not None and self.verbose:
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

    def save_artists(self, artists, filename="artist_lyrics", overwrite=False,
                     ensure_ascii=True):
        """Saves lyrics from multiple Artist objects as JSON object.

        Args:
            artists (:obj:`list`): List of :class:`Artist <types.Artist>`
                objects to save lyrics from.
            filename (:obj:`str`, optional): Name of the output file.
            overwrite (:obj:`bool`, optional): Overwrites preexisting file if `True`.
                Otherwise prompts user for input.
            ensure_ascii (:obj:`bool`, optional): If ensure_ascii is true
              (the default), the output is guaranteed to have all incoming
              non-ASCII characters escaped.

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
            json.dump(all_lyrics, outfile, ensure_ascii=ensure_ascii)

        # Delete the temporary directory
        shutil.rmtree(tmp_dir)
        elapsed = (time.time() - start) / 60 / 60
        print("Time elapsed: {t} hours".format(t=elapsed))
