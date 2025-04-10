from ..utils import convert_to_datetime
from .artist import Artist
from .base import BaseEntity


class Album(BaseEntity):
    """An album from the Genius.com database."""

    def __init__(self, client, json_dict, tracks):
        body = json_dict
        super().__init__(body["id"])
        self._body = body
        self._client = client
        self.artist = Artist(client, body["artist"])
        self.tracks = tracks
        self.release_date_components = convert_to_datetime(
            body.get("release_date_components")
        )

        self.api_path = body.get("api_path")
        self.cover_art_thumbnail_url = body.get("cover_art_thumbnail_url")
        self.cover_art_url = body.get("cover_art_url")
        self.full_title = body.get("full_title")
        self.name = body.get("name")
        self.name_with_artist = body.get("name_with_artist")
        self.url = body.get("url")

    def to_dict(self):
        body = super().to_dict()
        body["tracks"] = [track.to_dict() for track in self.tracks]
        return body

    def to_json(self, filename=None, sanitize=True, ensure_ascii=True):
        data = self.to_dict()

        return super().to_json(
            data=data, filename=filename, sanitize=sanitize, ensure_ascii=ensure_ascii
        )

    def to_text(self, filename=None, sanitize=True):
        data = "\n\n".join(
            f"[Song {n}: {track.song.title}]\n{track.song.lyrics}"
            for n, track in enumerate(self.tracks, start=1)
        ).strip()

        return super().to_text(data=data, filename=filename, sanitize=sanitize)

    def save_lyrics(
        self,
        filename=None,
        extension="json",
        overwrite=False,
        ensure_ascii=True,
        sanitize=True,
        verbose=True,
    ):
        if filename is None:
            filename = "Lyrics_" + self.name.replace(" ", "")

        return super().save_lyrics(
            filename=filename,
            extension=extension,
            overwrite=overwrite,
            ensure_ascii=ensure_ascii,
            sanitize=sanitize,
            verbose=verbose,
        )


class Track(BaseEntity):
    """docstring for Track"""

    def __init__(self, client, json_dict, lyrics):
        from .song import Song

        body = json_dict
        super().__init__(body["song"]["id"])
        self._body = body
        self.song = Song(client, body["song"], lyrics)

        self.number = body["number"]

    def to_dict(self):
        body = super().to_dict()
        body["song"] = self.song.to_dict()
        return body

    def to_json(self, filename=None, sanitize=True, ensure_ascii=True):
        data = self.to_dict()

        return super().to_json(
            data=data, filename=filename, sanitize=sanitize, ensure_ascii=ensure_ascii
        )

    def to_text(self, filename=None, sanitize=True):
        data = self.song.lyrics

        return super().to_text(data=data, filename=filename, sanitize=sanitize)

    def save_lyrics(
        self,
        filename=None,
        extension="json",
        overwrite=False,
        ensure_ascii=True,
        sanitize=True,
        verbose=True,
    ):
        if filename is None:
            filename = "Lyrics_{:02d}_{}".format(self.number, self.song.title)
            filename = filename.replace(" ", "")

        return super().save_lyrics(
            filename=filename,
            extension=extension,
            overwrite=overwrite,
            ensure_ascii=ensure_ascii,
            sanitize=sanitize,
            verbose=verbose,
        )

    def __repr__(self):
        name = self.__class__.__name__
        return "{}(number, song)".format(name)
