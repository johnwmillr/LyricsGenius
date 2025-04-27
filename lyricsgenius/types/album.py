from typing import Any

from ..utils import convert_to_datetime
from .artist import Artist
from .base import BaseEntity


class Track(BaseEntity):
    """docstring for Track"""

    from ..genius import Genius

    def __init__(self, client: Genius, body: dict[str, Any], lyrics: str) -> None:
        from .song import Song

        super().__init__(body["song"]["id"])
        self._body = body
        self.song = Song(client, body["song"], lyrics)
        self.number: int = body["number"]

    @property
    def _text_data(self) -> str:
        """Returns the text data for the track."""
        return self.song.lyrics

    def to_dict(self) -> dict[str, Any]:
        body = super().to_dict()
        body["song"] = self.song.to_dict()
        return body

    def to_json(
        self,
        filename: str | None = None,
        sanitize: bool = True,
        ensure_ascii: bool = True,
    ) -> str | None:
        return super().to_json(
            filename=filename, sanitize=sanitize, ensure_ascii=ensure_ascii
        )

    def to_text(self, filename: str | None = None, sanitize: bool = True) -> str | None:
        return super().to_text(filename=filename, sanitize=sanitize)

    def save_lyrics(
        self,
        filename: str | None = None,
        extension: str = "json",
        overwrite: bool = False,
        ensure_ascii: bool = True,
        sanitize: bool = True,
        verbose: bool = True,
    ) -> None:
        if filename is None:
            filename = f"Lyrics_{self.number:02d}_{self.song.title}".replace(" ", "")

        return super().save_lyrics(
            filename=filename,
            extension=extension,
            overwrite=overwrite,
            ensure_ascii=ensure_ascii,
            sanitize=sanitize,
            verbose=verbose,
        )

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return "{}(number, song)".format(name)


class Album(BaseEntity):
    """An album from the Genius.com database."""

    from ..genius import Genius

    def __init__(
        self, client: Genius, body: dict[str, Any], tracks: list[Track]
    ) -> None:
        super().__init__(body["id"])
        self._body = body
        self._client = client
        self.artist = Artist(client, body["artist"])
        self.tracks = tracks
        self.release_date_components = convert_to_datetime(
            body.get("release_date_components")
        )

        self.api_path: str = body["api_path"]
        self.cover_art_thumbnail_url: str = body["cover_art_thumbnail_url"]
        self.cover_art_url: str = body["cover_art_url"]
        self.full_title: str = body["full_title"]
        self.name: str = body["name"]
        self.name_with_artist: str = body["name_with_artist"]
        self.url: str = body["url"]

    @property
    def _text_data(self) -> str:
        return "\n\n".join(
            f"[Song {n}: {track.song.title}]\n{track.song.lyrics}"
            for n, track in enumerate(self.tracks, start=1)
        ).strip()

    def to_dict(self) -> dict[str, Any]:
        body = super().to_dict()
        body["tracks"] = [track.to_dict() for track in self.tracks]
        return body

    def to_json(
        self,
        filename: str | None = None,
        sanitize: bool = True,
        ensure_ascii: bool = True,
    ) -> str | None:
        return super().to_json(
            filename=filename, sanitize=sanitize, ensure_ascii=ensure_ascii
        )

    def to_text(self, filename: str | None = None, sanitize: bool = True) -> str | None:
        return super().to_text(filename=filename, sanitize=sanitize)

    def save_lyrics(
        self,
        filename: str | None = None,
        extension: str = "json",
        overwrite: bool = False,
        ensure_ascii: bool = True,
        sanitize: bool = True,
        verbose: bool = True,
    ) -> None:
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
