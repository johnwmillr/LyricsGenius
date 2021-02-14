# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

from filecmp import cmp

from .base import BaseEntity, Stats
from .artist import Artist


class Song(BaseEntity):
    """A song from the Genius.com database."""

    def __init__(self, client, json_dict, lyrics=""):
        body = json_dict
        super().__init__(body['id'])
        self._body = body
        self._client = client
        self.artist = body['primary_artist']['name']
        self.lyrics = lyrics if lyrics else ""
        self.primary_artist = Artist(client, body['primary_artist'])
        self.stats = Stats(body['stats'])

        self.annotation_count = body['annotation_count']
        self.api_path = body['api_path']
        self.full_title = body['full_title']
        self.header_image_thumbnail_url = body['header_image_thumbnail_url']
        self.header_image_url = body['header_image_url']
        self.lyrics_owner_id = body['lyrics_owner_id']
        self.lyrics_state = body['lyrics_state']
        self.path = body['path']
        self.pyongs_count = body['pyongs_count']
        self.song_art_image_thumbnail_url = body['song_art_image_thumbnail_url']
        self.song_art_image_url = body['song_art_image_url']
        self.title = body['title']
        self.title_with_featured = body['title_with_featured']
        self.url = body['url']

    def to_dict(self):
        body = super().to_dict()
        body['artist'] = self.artist
        body['lyrics'] = self.lyrics
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
        data = self.lyrics

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

        if filename is None:
            filename = "Lyrics_{}_{}".format(self.artist.replace(" ", ""),
                                             self.title.replace(" ", "")
                                             ).lower()

        return super().save_lyrics(filename=filename,
                                   extension=extension,
                                   overwrite=overwrite,
                                   ensure_ascii=ensure_ascii,
                                   sanitize=sanitize,
                                   verbose=verbose)

    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else:
            lyr = self.lyrics[:100]
        return '"{title}" by {artist}:\n    {lyrics}'.format(
            title=self.title, artist=self.artist, lyrics=lyr.replace('\n', '\n    '))

    def __cmp__(self, other):
        return (cmp(self.title, other.title)
                and cmp(self.artist, other.artist)
                and cmp(self.lyrics, other.lyrics))
