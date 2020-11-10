from ..utils import convert_to_datetime
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
        if filename is None:
            filename = 'Lyrics_' + self.name.replace(' ', '')

        return super().save_lyrics(filename=filename,
                                   extension=extension,
                                   overwrite=overwrite,
                                   ensure_ascii=ensure_ascii,
                                   sanitize=sanitize,
                                   verbose=verbose)
