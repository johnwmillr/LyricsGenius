# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import os
import json
from lyricsgenius.utils import sanitize_filename


class Artist(object):
    """An artist with songs from the Genius.com database."""

    def __init__(self, json_dict):
        """ Artist Constructor

        Properties:
            name: Artist name.
            image_url: URL to the artist image on Genius.com
            songs: List of the artist's Song objects
            num_songs: Number of songs in the Artist object

        Methods:
            add_song: Add a song to the Artist object
            save_lyrics: Save the lyrics to a JSON or TXT file
        """
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
        return self._body['name']

    @property
    def image_url(self):
        if 'image_url' in self._body:
            return self._body['image_url']

    @property
    def songs(self):
        return self._songs

    @property
    def num_songs(self):
        return self._num_songs

    def add_song(self, new_song, verbose=True):
        """Add a Song object to the Artist object"""

        if any([song.title == new_song.title for song in self._songs]):
            if verbose:
                print('{s} already in {a}, not adding song.'.format(s=new_song.title,
                                                                    a=self.name))
            return 1  # Failure
        if new_song.artist == self.name:
            self._songs.append(new_song)
            self._num_songs += 1
            return 0  # Success
        if verbose:
            print("Can't add song by {b}, artist must be {a}.".format(b=new_song.artist,
                                                                      a=self.name))
        return 1  # Failure

    def get_song(self, song_name):
        """Search Genius.com for *song_name* and add it to artist"""
        raise NotImplementedError("I need to figure out how to allow Artist() to access Genius.search_song().")
        # song = Genius.search_song(song_name, self.name)
        # self.add_song(song)
        # return

    def to_json(self,
                filename=None,
                sanitize=True):
        """
        Convert the Song object to a json string.
        INPUT
        :filename: Output filename, string. If not specified, the
                   result is returned as a string.
        :sanitize: Sanitizes the filename if True.

        OUTPUT
            If `filename` is None, returns the lyrics as
            a plain string. Otherwise None.
        """
        data = self._body
        data['songs'] = [song._body for song in self.songs]

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
        """
        Convert all song lyrics to a single string.
        INPUT
        :filename: Output filename, string. If not specified, the
                   result is returned as a string.
        :binary_encoding: Enable binary encoding of text data.
        :sanitize: Sanitizes the filename if True.

        OUTPUT
            If `filename` is None, returns the lyrics as
            a plain string. Otherwise None.
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
                    sanitize=True,
                    verbose=True):
        """Saves all lyrics within an Artist object to a single file."""
        extension = extension.lstrip(".").lower()
        assert (extension == 'json') or (extension == 'txt'), "extension must be JSON or TXT"

        # Determine the filename
        if not filename:
            filename = 'Lyrics_' + self.name.replace(' ', '') + '.' + extension
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
            self.to_json(filename)
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
        msg = repr((self.name, msg[:-1])) if self._num_songs == 1 else repr((self.name, msg))
        return msg
