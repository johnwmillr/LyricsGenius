# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import json
import os
from filecmp import cmp
from lyricsgenius.utils import sanitize_filename


class Song(object):
    """A song from the Genius.com database.

    Returns:
        :class:`Song`
    """

    def __init__(self, json_dict, lyrics=''):
        # Song Constructor
        self._body = json_dict['song'] if 'song' in json_dict else json_dict
        self._body['lyrics'] = lyrics
        self._url = self._body['url']
        self._api_path = self._body['api_path']
        self._id = self._body['id']

    @property
    def title(self):
        """Title of the song.

        Returns:
            :obj:`str`

        """
        return self._body.get('title')

    @property
    def artist(self):
        """Primary artist on the song.

        Returns:
            :obj:`str`

        """
        primary = self._body.get('primary_artist')
        if primary:
            return primary.get('name')

    @property
    def lyrics(self):
        """Full set of song lyrics.

        Returns:
            :obj:`str`

        """
        return self._body.get('lyrics')

    @property
    def album(self):
        """Name of the album the song is on.

        Returns:
            :obj:`str` | :obj:`None`

        """
        album = self._body.get('album')
        if album:
            return album.get('name')

    @property
    def year(self):
        """Year the song was released.

        Returns:
            :obj:`str`

        """
        return self._body.get('release_date')

    @property
    def url(self):
        """URL to the song on Genius.

        Returns:
            :obj:`str`

        """
        return self._body.get('url')

    @property
    def album_url(self):
        """URL to the song album.

        Returns:
            :obj:`str` | :obj:`None`

        """
        album = self._body.get('album')
        if album:
            return album.get('url')

    @property
    def featured_artists(self):
        """Artists featured on the song.

        Returns:
            :obj:`list`

        """
        return self._body.get('featured_artists')

    @property
    def producer_artists(self):
        """Producers of the song.

        Returns:
            :obj:`list`

        """
        return self._body.get('producer_artists')

    @property
    def media(self):
        """External IDs of the song.
        For example song's YouTube link, Spotify ID and link.

        Returns:
            :obj:`list`

        """
        return self._body.get('media')

    @property
    def writer_artists(self):
        """List of artists credited as writers.

        Returns:
            :obj:`list`

        """
        return self._body.get('writer_artists')

    @property
    def song_art_image_url(self):
        """URL to the song's cover art.

        Returns:
            :obj:`str`

        """
        return self._body.get('song_art_image_url')

    def to_dict(self):
        """Creates a dictionary from the song object.
        Used in :func:`save_lyrics` to create json object.

        Returns:
            :obj:`dict`

        """
        return dict({'title': self.title,
                     'album': self.album,
                     'year': self.year,
                     'lyrics': self.lyrics,
                     'image': self.song_art_image_url})

    def to_json(self,
                filename=None,
                full_data=True,
                sanitize=True,
                ensure_ascii=True):
        """Converts the Song object to a json string.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            full_data (:obj:`str`): Provides full song metadata when set to `True`.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.
            ensure_ascii (:obj:`bool`, optional): If ensure_ascii is true
              (the default), the output is guaranteed to have all incoming
              non-ASCII characters escaped.

        Returns:
            :obj:`str` \\| :obj:`None`: If filename is None, returns the lyrics as
            a plain string, otherwise None.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and thefore cause the saving to fail.

        """
        data = self._body if full_data else self.to_dict()

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
        """Saves the song lyrics as a text file.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            binary_encoding (:obj:`bool`, optional): Enables binary encoding
                of text data.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.

        Returns:
            :obj:`str` \\| :obj:`None`: If :obj:`filename` is
            `None`, returns the lyrics as a plain string, otherwise `None`.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and thefore cause the saving to fail.

        """
        data = self.lyrics

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
                    overwrite=None,
                    binary_encoding=False,
                    ensure_ascii=True,
                    full_data=True,
                    sanitize=True,
                    verbose=True):
        """Save Song lyrics and metadata to a JSON or TXT file.

        If the extension is 'json' (which the default), the lyrics will be saved
        alongside the song's information. Take a look at the example below.

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
            full_data (:obj:`str`): Provides full song metadata when set to `True`.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.
            verbose (:obj:`bool`, optional): prints operation result.

        Examples:
            .. code:: python

                # getting songs lyrics from saved JSON file
                import json
                with open('song.json', 'r') as f:
                    data = json.load(f)

                print(data['lyrics'])

        Note:
            If :obj:`full_data` is set to `False`, only the following attributes
            of the song will be available: :obj:`title`, :attr:`album`, :attr:`year`,
            :attr:`lyrics`, and :attr:`song_art_image_url`

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and thefore cause the saving to fail.

        """
        extension = extension.lstrip(".").lower()
        msg = "extension must be JSON or TXT"
        assert (extension == 'json') or (extension == 'txt'), msg

        # Determine the filename
        if filename:
            for ext in ["txt", "TXT", "json", "JSON"]:
                filename = filename.replace("." + ext, "")
            filename += "." + extension
        else:
            filename = "Lyrics_{}_{}.{}".format(self.artist.replace(" ", ""),
                                                self.title.replace(" ", ""),
                                                extension).lower()
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
            self.to_json(filename, full_data=full_data, sanitize=sanitize,
                         ensure_ascii=ensure_ascii)
        else:
            self.to_text(filename, binary_encoding=binary_encoding, sanitize=sanitize)

        if verbose:
            print('Wrote {} to {}.'.format(self.title, filename))
        return None

    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else:
            lyr = self.lyrics[:100]
        return '"{title}" by {artist}:\n    {lyrics}'.format(
            title=self.title, artist=self.artist, lyrics=lyr.replace('\n', '\n    '))

    def __repr__(self):
        return repr((self.title, self.artist))

    def __cmp__(self, other):
        return (cmp(self.title, other.title)
                and cmp(self.artist, other.artist)
                and cmp(self.lyrics, other.lyrics))
