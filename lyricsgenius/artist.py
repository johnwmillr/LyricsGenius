# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import json
import os


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

    def add_song(self, newsong, verbose=True):
        """Add a Song object to the Artist object"""

        if any([song.title == newsong.title for song in self._songs]):
            if verbose:
                print('{s} already in {a}, not adding song.'.format(s=newsong.title,
                                                                    a=self.name))
            return 1  # Failure
        if newsong.artist == self.name:
            self._songs.append(newsong)
            self._num_songs += 1
            return 0  # Success
        if verbose:
            print("Can't add song by {b}, artist must be {a}.".format(b=newsong.artist,
                                                                      a=self.name))
        return 1  # Failure

    def get_song(self, song_name):
        """Search Genius.com for *song_name* and add it to artist"""
        raise NotImplementedError("I need to figure out how to allow Artist() to access Genius.search_song().")
        # song = Genius.search_song(song_name, self.name)
        # self.add_song(song)
        # return

    # TODO: define an export_to_json() method

    def save_lyrics(self, filename=None, format_='json', overwrite=False,
                    skip_duplicates=True, verbose=True, binary_encoding=False):
        """Allows user to save all lyrics within an Artist obejct"""
        format_ = format_.lstrip(".")
        assert (format_ == 'json') or (format_ == 'txt'), "format_ must be JSON or TXT"

        # We want to reject songs that have already been added to artist collection
        def songsAreSame(s1, s2):
            from difflib import SequenceMatcher as sm
            # Idea credit: https://bigishdata.com/2016/10/25/
            seqA = sm(None, s1.lyrics, s2['lyrics'])
            if seqA.ratio() > 0.4:
                seqB = sm(None, s2['lyrics'], s1.lyrics)
                return seqA.ratio() > 0.5 or seqB.ratio() > 0.5
            return False

        def songInArtist(new_song):
            # artist_lyrics is global (works in Jupyter notebook)
            for song in lyrics_to_write['songs']:
                if songsAreSame(new_song, song):
                    return True
            return False

        # Determine the filename
        if filename:
            # Remove format suffix if supplied by user
            for ext in ["txt", "TXT", "json", "JSON"]:
                filename = filename.replace("." + ext, "")
            filename += "." + format_
        else:
            filename = "Lyrics_{}.{}".format(self.name.replace(" ", ""), format_)

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
        if format_ == 'json':
            lyrics_to_write = {'songs': [], 'artist': self.name}
            for song in self.songs:
                # This takes way too long! It's basically O(n^2), can I do better?
                if skip_duplicates is False or not songInArtist(song):
                    lyrics_to_write['songs'].append({})
                    lyrics_to_write['songs'][-1]['title'] = song.title
                    lyrics_to_write['songs'][-1]['album'] = song.album
                    lyrics_to_write['songs'][-1]['year'] = song.year
                    lyrics_to_write['songs'][-1]['lyrics'] = song.lyrics
                    lyrics_to_write['songs'][-1]['image'] = song.song_art_image_url
                    lyrics_to_write['songs'][-1]['artist'] = self.name
                    lyrics_to_write['songs'][-1]['raw'] = song._body
                else:
                    self._songs_dropped += 1
                    if verbose:
                        print("SKIPPING \"{}\" (already found in artist collection)".format(song.title))
        else:
            lyrics_to_write = " ".join([s.lyrics + 5*'\n' for s in self.songs])

        if binary_encoding:
            lyrics_to_write = lyrics_to_write.encode('utf8')

        # Write the lyrics to either a .json or .txt file
        if write_file:
            with open(filename, 'wb' if binary_encoding else 'w') as lyrics_file:
                if format_ == 'json':
                    json.dump(lyrics_to_write, lyrics_file)
                else:
                    lyrics_file.write(lyrics_to_write)
            if verbose:
                print('Wrote {} songs to {}.'.format(self.num_songs - self._songs_dropped, filename))
        else:
            if verbose:
                print('Skipping file save.\n')
        return lyrics_to_write

    def __str__(self):
        """Return a string representation of the Artist object."""
        msg = "{name}, {num} songs".format(name=self.name, num=self._num_songs)
        msg = msg[:-1] if self._num_songs == 1 else msg
        return msg

    def __repr__(self):
        msg = "{num} songs".format(num=self._num_songs)
        msg = repr((self.name, msg[:-1])) if self._num_songs == 1 else repr((self.name, msg))
        return msg
