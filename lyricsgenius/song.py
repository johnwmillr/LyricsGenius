# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import json
import os
from filecmp import cmp


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

    def _sanitize_filename(self, f):
        keepchars = (" ", ".", "_")
        return "".join(c for c in f if c.isalnum() or c in keepchars).rstrip()

    def save_lyrics(self, filename=None, extension='json', verbose=True,
                    overwrite=None, binary_encoding=False):
        """Allows user to save song lyrics from Song object to a .json or .txt file."""
        extension = extension.lstrip(".")
        assert (extension == 'json') or (extension == 'txt'), "format_ must be JSON or TXT"

        # Determine the filename
        if filename:
            for ext in ["txt", "TXT", "json", "JSON"]:
                filename = filename.replace("." + ext, "")
            filename += "." + extension
        else:
            filename = "Lyrics_{}_{}.{}".format(self.artist.replace(" ", ""),
                                                self.title.replace(" ", ""),
                                                extension).lower()
            filename = self._sanitize_filename(filename)

        # Check if file already exists
        write_file = False
        if not os.path.isfile(filename):
            write_file = True
        elif overwrite:
            write_file = True
        else:
            if input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower() == 'y':
                write_file = True

        # Format lyrics as either .txt or .json
        if extension == 'json':
            lyrics_to_write = {'songs': [], 'artist': self.artist}
            lyrics_to_write['songs'].append(self.to_dict())
        else:
            lyrics_to_write = self.lyrics

        if binary_encoding:
            lyrics_to_write = lyrics_to_write.encode('utf8')

        # Write the lyrics to either a .json or .txt file
        if write_file:
            with open(filename, 'wb' if binary_encoding else 'w') as lyrics_file:
                if extension == 'json':
                    json.dump(lyrics_to_write, lyrics_file)
                else:
                    lyrics_file.write(lyrics_to_write)
            if verbose:
                print('Wrote {} to {}.'.format(self.title, filename))
        else:
            if verbose:
                print('Skipping file save.\n')
        return lyrics_to_write

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
