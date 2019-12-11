# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import json
import os
from filecmp import cmp
from lyricsgenius.utils import sanitize_filename


class Song(object):
    """A song from the Genius.com database."""

    def __init__(self, json_dict, lyrics=''):
        """ Song Constructor

        Properties:
            title: Title of the song.
            artist: Primary artist on the song.
            lyrics: Full set of song lyrics.
            album: Name of the album the song is on.
            year: Year the song was released.

        Methods:
            save_lyrics: Save the song lyrics to a JSON or TXT file.
        """
        self._body = json_dict['song'] if 'song' in json_dict else json_dict
        self._body['lyrics'] = lyrics
        self._url = self._body['url']
        self._api_path = self._body['api_path']
        self._id = self._body['id']

    @property
    def title(self):
        return self._body.get('title')

    @property
    def artist(self):
        primary = self._body.get('primary_artist')
        if primary:
            return primary.get('name')

    @property
    def lyrics(self):
        return self._body.get('lyrics')

    @property
    def album(self):
        album = self._body.get('album')
        if album:
            return album.get('name')

    @property
    def year(self):
        return self._body.get('release_date')

    @property
    def url(self):
        return self._body.get('url')

    @property
    def album_url(self):
        album = self._body.get('album')
        if album:
            return album.get('url')

    @property
    def featured_artists(self):
        return self._body.get('featured_artists')

    @property
    def producer_artists(self):
      return self._body.get('producer_artists')

    @property
    def media(self):
        return self._body.get('media')

    @property
    def writer_artists(self):
        """List of artists credited as writers"""
        return self._body.get('writer_artists')

    @property
    def song_art_image_url(self):
        return self._body.get('song_art_image_url')

    def to_dict(self):
        """
        Create a dictionary from the song object
        Used in save_lyrics to create json object

        :return: Dictionary
        """
        return dict({'title': self.title,
                     'album': self.album,
                     'year': self.year,
                     'lyrics': self.lyrics,
                     'image': self.song_art_image_url})

    def to_json(self,
                filename=None,
                full_data=True,
                sanitize=True):
        """
        Convert the Song object to a json string.
        INPUT
        :filename: Output filename, string. If not specified, the
                   result is returned as a string.
        :full_data: Provides full song metadata when set to True.
        :sanitize: Sanitizes the filename if True.

        OUTPUT
            If `filename` is None, returns the lyrics as
            a plain string. Otherwise None.
        """
        data = self._body if full_data else self.to_dict()

        # Return the json string if no output path was specified
        if not filename:
            return json.dumps(data, indent=1)

        # Save Song object to a json file
        filename = sanitize_filename(filename) if sanitize else filename
        with open(filename, 'w') as ff:
            json.dump(data, ff, indent=1)
        return None

    def to_text(self,
                filename=None,
                binary_encoding=False,
                sanitize=True):
        """Save the song lyrics as a text file.
        INPUT
        :filename: Output filename. If not specified, the result is
                   return as a string.
        :binary_encoding: Enable binary encoding of text data.
        :sanitize: Sanitizes the filename if True.

        OUTPUT
            If `filename` is None, returns the lyrics as
            a plain string. Otherwise None.
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
                    full_data=True,
                    sanitize=True,
                    verbose=True):
        """Save Song lyrics and metadata to a JSON or TXT file."""
        extension = extension.lstrip(".").lower()
        assert (extension == 'json') or (extension == 'txt'), "extension must be JSON or TXT"

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
            if input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower() == 'y':
                write_file = True

        # Exit if we won't be saving a file
        if not write_file:
            if verbose:
                print('Skipping file save.\n')
            return

        # Save the lyrics to a file
        if extension == 'json':
            self.to_json(filename, full_data=full_data)
        else:
            self.to_text(filename, binary_encoding=binary_encoding)

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
        return cmp(self.title, other.title) and cmp(self.artist, other.artist) and cmp(self.lyrics, other.lyrics)
