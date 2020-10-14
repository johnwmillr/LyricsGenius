import os

from ..utils import sanitize_filename, convert_to_datetime
from .base import BaseEntity
from .artist import Artist


class Album(BaseEntity):
    """An album from the Genius.com database.

    Attributes:
        _type (:obj:`str`)
        api_path (:obj:`str`)
        artist (:class:`Artist`)
        cover_art_thumbnail_url (:obj:`str`)
        cover_art_url (:obj:`str`)
        full_title (:obj:`str`)
        id (:obj:`int`)
        name (:obj:`str`)
        name_with_artist (:obj:`str`)
        release_date_components (:class:`datetime`)
        songs (:obj:`list`):
            A list of :class:`Song` objects.
        url (:obj:`str`)
    """

    def __init__(self, client, json_dict, songs):
        body = json_dict
        super().__init__(body['id'])
        self._body = body
        self._client = client
        self.artist = Artist(client, body['artist'])
        self.songs = songs
        self.release_date_components = convert_to_datetime(
            body['release_date_components']
        )

        self._type = body['_type']
        self.api_path = body['api_path']
        self.cover_art_thumbnail_url = body['cover_art_thumbnail_url']
        self.cover_art_url = body['cover_art_url']
        self.full_title = body['full_title']
        self.name = body['name']
        self.name_with_artist = body['name_with_artist']
        self.url = body['url']

    def to_dict(self):
        body = super().to_dict()
        body['songs'] = [song.to_dict() for song in self.songs]
        return body

    def to_json(self,
                filename=None,
                sanitize=True,
                ensure_ascii=True):
        data = self.to_dict()

        return super().to_json(data=data,
                               filename=filename,
                               sanitize=sanitize,
                               ensure_ascii=ensure_ascii)

    def to_text(self,
                filename=None,
                binary_encoding=False,
                sanitize=True):
        data = ' '.join(song.lyrics for song in self.songs)

        return super().to_text(data=data,
                               filename=filename,
                               binary_encoding=binary_encoding,
                               sanitize=sanitize)

    def save_lyrics(self,
                    filename=None,
                    extension='json',
                    overwrite=False,
                    binary_encoding=False,
                    ensure_ascii=True,
                    sanitize=True,
                    verbose=True):
        """Saves all lyrics within an Album object to a single file.
        If the extension is 'json', the method will save album information and
        album songs.
        If you only want the songs lyrics, set :obj:`extension` to `txt`.
        If you choose to go with JSON (which is the default extension), you can access
        the lyrics by accessing the :class:`Song <types.Song>`
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
