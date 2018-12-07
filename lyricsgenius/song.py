# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import json
import os


class Song(object):
    """A song from the Genius.com database."""

    def __init__(self, json_dict, lyrics=''):
        """ Song Constructor

        Properties:
            title: Title of the song.
            artist: Primary artist on the song.
            lyrcis: Full set of song lyrics.
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

    def save_lyrics(self, filename=None, format_='txt', verbose=True,
                    overwrite=False, binary_encoding=False):
        # TODO: way too much repeated code between this and the Artist.save_lyrics method
        """Allows user to save song lyrics from Song obejct to a .json or .txt file."""
        format_ = format_.lstrip(".")
        assert (format_ == 'json') or (format_ == 'txt'), "format_ must be JSON or TXT"

        # Determine the filename
        if filename:
            # Remove format suffix if supplied by user
            for ext in ["txt", "TXT", "json", "JSON"]:
                filename = filename.replace("." + ext, "")
            filename += "." + format_
        else:
            filename = "Lyrics_{}.{}".format(self.artist.replace(" ", ""), format_)

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
            lyrics_to_write = {'songs': [], 'artist': self.artist}
            lyrics_to_write['songs'].append({})
            lyrics_to_write['songs'][-1]['title'] = self.title
            lyrics_to_write['songs'][-1]['album'] = self.album
            lyrics_to_write['songs'][-1]['year'] = self.year
            lyrics_to_write['songs'][-1]['lyrics'] = self.lyrics
            lyrics_to_write['songs'][-1]['image'] = self.song_art_image_url
            lyrics_to_write['songs'][-1]['artist'] = self.artist
            lyrics_to_write['songs'][-1]['json'] = self._body
        else:
            lyrics_to_write = self.lyrics

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
