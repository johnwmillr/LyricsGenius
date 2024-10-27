# LyricsGenius
# copyright 2024 john w. miller
# See LICENSE for details.

"""Artist object"""
import logging

from .base import BaseEntity
from ..utils import safe_unicode


class Artist(BaseEntity):
    """An artist with songs from the Genius.com database."""
    logger = logging.getLogger(__name__)

    def __init__(self, client, json_dict):
        # Artist Constructor
        body = json_dict
        super().__init__(body['id'])
        self._body = body
        self._client = client
        self.songs = []
        self.num_songs = len(self.songs)

        self.api_path = body['api_path']
        self.header_image_url = body['header_image_url']
        self.image_url = body['image_url']
        # self.iq = body['iq']
        self.is_meme_verified = body['is_meme_verified']
        self.is_verified = body['is_verified']
        self.name = body['name']
        self.url = body['url']

    def __len__(self):
        return len(self.songs)

    def add_song(self, new_song, verbose=True, include_features=False):
        """Adds a song to the Artist.

        This method adds a new song to the artist object. It checks
        if the song is already in artist's songs and whether the
        song's artist is the same as the `Artist` object.

        Args:
            new_song (:class:`Song <lyricsgenius.types.Song>`): Song to be added.
            verbose (:obj:`bool`, optional): Does nothing.
                Kept for backward compatibility.
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
                return None
        if any([song.title == new_song.title for song in self.songs]):
            self.logger.info('%s already in %s, not adding song.',
                             safe_unicode(new_song.title),
                             safe_unicode(self.name))
            return None
        if (new_song.artist == self.name
                or (include_features and any(new_song._body['featured_artists']))):
            self.songs.append(new_song)
            self.num_songs += 1
            return new_song
            self.logger.info("Can't add song by %s, artist must be %s.",
                             safe_unicode(new_song.artist),
                             safe_unicode(self.name))
        return None

    def song(self, song_name):
        """Gets the artist's song.

        If the song is in the artist's songs, returns the song. Otherwise searches
        Genius for the song and then returns the song.

        Args:
            song_name (:obj:`str`): name of the song.
                the result is returned as a string.

        Returns:
            :obj:`Song <types.Song>` \\|‌ :obj:`None`: If it can't find the song,
            returns *None*.

        """
        for song in self.songs:
            if song.title == song_name:
                return song
        self.logger.info("'%s' was not in %s's songs.",
                         safe_unicode(song_name),
                         safe_unicode(self.name))
        song = self._client.search_song(song_name, self.name)
        return song

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
                sanitize=True):
        data = ' '.join(song.lyrics for song in self.songs)
        return super().to_text(data=data,
                               filename=filename,
                               sanitize=sanitize)

    def save_lyrics(self,
                    filename=None,
                    extension='json',
                    overwrite=False,
                    ensure_ascii=True,
                    sanitize=True,
                    verbose=True):
        # Determine the filename
        if filename is None:
            filename = 'Lyrics_' + self.name.replace(' ', '')

        return super().save_lyrics(filename=filename,
                                   extension=extension,
                                   overwrite=overwrite,
                                   ensure_ascii=ensure_ascii,
                                   sanitize=sanitize)

    def __str__(self):
        """Return a string representation of the Artist object."""
        msg = "{name}, {num} songs".format(name=self.name, num=self.num_songs)
        msg = msg[:-1] if self.num_songs == 1 else msg
        return msg
