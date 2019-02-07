# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.


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
        return 1

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

    # TODO: define an export_to_json() method

    def save_lyrics(self, extension='json', overwrite=False,
                    verbose=True, binary_encoding=False):
        """Allows user to save all lyrics within an Artist object"""
        extension = extension.lstrip(".")
        assert (extension == 'json') or (extension == 'txt'), "format_ must be JSON or TXT"

        for song in self.songs:
            song.save_lyrics(extension=extension, overwrite=overwrite, verbose=verbose, binary_encoding=binary_encoding)

    def __str__(self):
        """Return a string representation of the Artist object."""
        msg = "{name}, {num} songs".format(name=self.name, num=self._num_songs)
        msg = msg[:-1] if self._num_songs == 1 else msg
        return msg

    def __repr__(self):
        msg = "{num} songs".format(num=self._num_songs)
        msg = repr((self.name, msg[:-1])) if self._num_songs == 1 else repr((self.name, msg))
        return msg
