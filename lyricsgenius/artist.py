# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

"""Artist object"""

import os
import json
from lyricsgenius.utils import sanitize_filename


class Artist(object):
    """An artist with songs from the Genius.com database.

    Returns:
        :class:`Artist`: Artist object contatining artist data
        and song lyrics.

    """

    def __init__(self, client, json_dict):
        # Artist Constructor

        self._client = client
        self._body = json_dict['artist']
        self._url = self._body['url']
        self._api_path = self._body['api_path']
        self._id = self._body['id']
        self._songs = []
        self._num_songs = len(self._songs)
        self._songs_dropped = 0

    def __len__(self):
        return len(self._songs)

    @property
    def name(self):
        """Artist's name.

        Returns:
            :obj:`str`

        """
        return self._body['name']

    @property
    def image_url(self):
        """URL to the artist's image

        Returns:
            :obj:`str` | :obj:`None`

        """
        if 'image_url' in self._body:
            return self._body['image_url']

    @property
    def songs(self):
        """Song objects saved for the artist.

        Returns:
            :obj:`list`: A list contatining :class:`Song <song.Song>`
            objects.

        """
        return self._songs

    @property
    def num_songs(self):
        """Number of the songs in the Artist object.
        Equivolant to `len(artist.songs)`

        Returns:
            :obj:`int`

        """
        return self._num_songs

    def add_song(self, new_song, verbose=True, include_features=False):
        """Adds a song to the Artist.

        This method adds a new song to the artist object. It checks
        if the song is already in artist's songs and whether the
        song's artist is the same as the `Artist` object.

        Args:
            new_song (:class:`Song <lyricsgenius.song.Song>`): Song to be added.
            verbose (:obj:`bool`, optional): prints operation result.
            include_features (:obj:`bool`, optional): If True, includes tracks
                featuring the artist.

        Returns:
            :obj:`int`: 0 for success and 1 for failure.

        Examples:
            .. code:: python

                genius = Genius(token)
                artist = genius.search_artist('Andy Shauf', max_songs=3)

                # Way 1
                song = genius.search_song('To You', artist.name)
                artist.add_song(song)

                # Way 2
                artist.add_song('To You')

        """
        if isinstance(new_song, str):
            new_song = self._client.search_song(new_song)
            if new_song is None:
                return 1  # Failure
        if any([song.title == new_song.title for song in self._songs]):
            if verbose:
                print('{s} already in {a}, not adding song.'.format(s=new_song.title,
                                                                    a=self.name))
            return 1  # Failure
        if (new_song.artist == self.name
                or (include_features and any(new_song.featured_artists))):
            self._songs.append(new_song)
            self._num_songs += 1
            return 0  # Success
        if verbose:
            print("Can't add song by {b}, artist must be {a}.".format(b=new_song.artist,
                                                                      a=self.name))
        return 1  # Failure

    def song(self, song_name):
        """Gets the artist's song.

        If the song is in the artist's songs, returns the song. Otherwise searches
        Genius for the song and then returns the song.

        Args:
            song_name (:obj:`str`): name of the song.
                the result is returned as a string.
            sanitize (:obj:`bool`): Sanitizes the filename if `True`.

        Returns:
            :obj:`Song <song.Song>` \\|‌ :obj:`None`: If it can't find the song,
                returns *None*.

        """
        for song in self.songs:
            if song.title == song_name:
                return song

        song = self._client.search_song(song_name, self.name)
        return song

    def to_json(self,
                filename=None,
                sanitize=True,
                ensure_ascii=True):
        """Converts the Song object to a json string.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.
            ensure_ascii (:obj:`bool`, optional): If ensure_ascii is true
              (the default), the output is guaranteed to have all incoming
              non-ASCII characters escaped.

        Returns:
            :obj:`str` \\|‌ :obj:`None`: If :obj:`filename` is `None`,
            returns the lyrics as a plain string, otherwise `None`.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and thefore cause the saving to fail.

        """
        data = self._body
        data['songs'] = [song._body for song in self.songs]

        # Return the json string if no output path was specified
        if not filename:
            return json.dumps(data, indent=1, ensure_ascii=ensure_ascii)

        # Save Song object to a json file
        filename = sanitize_filename(filename) if sanitize else filename
        with open(filename, 'w') as ff:
            json.dump(data, ff, indent=1, ensure_ascii=ensure_ascii)
        return None

    def to_text(self,
                filename=None,
                binary_encoding=False,
                sanitize=True):
        """Converts all song lyrics to a single string.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            binary_encoding (:obj:`bool`, optional): Enables binary encoding
                of text data.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.

        Returns:
            :obj:`str` \\| ‌:obj:`None`: If :obj:`filename` is `None`,
            returns the lyrics as a plain string. Otherwise `None`.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and thefore cause the saving to fail.

        """
        data = ' '.join(song.lyrics for song in self.songs)

        # Return the lyrics as a string if no `filename` was specified
        if not filename:
            return data

        # Save song lyrics to a text file
        filename = sanitize_filename(filename) if sanitize else filename
        with open(filename, 'wb' if binary_encoding else 'w') as ff:
            if binary_encoding:
                data = data.encode('utf8')
            ff.write(data)
        return None

    def save_lyrics(self,
                    filename=None,
                    extension='json',
                    overwrite=False,
                    binary_encoding=False,
                    ensure_ascii=True,
                    sanitize=True,
                    verbose=True):
        """Saves all lyrics within an Artist object to a single file.
        If the extension is 'json', the method will save artist information and
        artist songs.
        If you only want the songs lyrics, set :obj:`extension` to `txt`.
        If you choose to go with JSON (which is the default extension), you can access
        the lyrics by accessing the :class:`Song <song.Song>`
        objects inside the `songs` key of the JSON file.
        Take a look at the example below.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            extension (:obj:`str`, optional): Format of the file (`json` or `txt`).
            overwrite (:obj:`bool`, optional): Overwrites preexisting file if `True`.
                Otherwise prompts user for input.
            binary_encoding (:obj:`bool`, optional): Enables binary encoding
                of text data.
            ensure_ascii (:obj:`bool`, optional): If ensure_ascii is true
                (the default), the output is guaranteed to have all incoming
                non-ASCII characters escaped.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.
            verbose (:obj:`bool`, optional): prints operation result.

        Examples:
            .. code:: python

                # getting songs lyrics from saved JSON file
                import json
                with open('file.json', 'r') as f:
                    data = json.load(f)

                for song in data['songs']:
                    print(song.lyrics)

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and thefore cause the saving process to fail.

        """
        extension = extension.lstrip(".").lower()
        msg = "extension must be JSON or TXT"
        assert (extension == 'json') or (extension == 'txt'), msg

        # Determine the filename
        if not filename:
            filename = 'Lyrics_' + self.name.replace(' ', '') + '.' + extension
        filename = sanitize_filename(filename) if sanitize else filename

        # Check if file already exists
        write_file = False
        if overwrite or not os.path.isfile(filename):
            write_file = True
        elif verbose:
            msg = "{} already exists. Overwrite?\n(y/n): ".format(filename)
            if input(msg).lower() == 'y':
                write_file = True

        # Exit if we won't be saving a file
        if not write_file:
            if verbose:
                print('Skipping file save.\n')
            return

        # Save the lyrics to a file
        if extension == 'json':
            self.to_json(filename, ensure_ascii=ensure_ascii)
        else:
            self.to_text(filename, binary_encoding=binary_encoding)

        if verbose:
            print('Wrote `{}`'.format(filename))
        return None

    def __str__(self):
        """Return a string representation of the Artist object."""
        msg = "{name}, {num} songs".format(name=self.name, num=self._num_songs)
        msg = msg[:-1] if self._num_songs == 1 else msg
        return msg

    def __repr__(self):
        msg = "{num} songs".format(num=self._num_songs)
        msg = (repr((self.name, msg[:-1]))
               if self._num_songs == 1
               else repr((self.name, msg)))
        return msg
