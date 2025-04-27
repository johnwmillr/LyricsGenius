# LyricsGenius
# copyright 2025 John W. R. Miller
# See LICENSE for details.

from filecmp import cmp
from typing import Any

from .album import Album
from .artist import Artist
from .base import BaseEntity, Stats


class Song(BaseEntity):
    """A song from the Genius.com database."""

    from ..genius import Genius

    def __init__(self, client: Genius, body: dict[str, Any], lyrics: str = "") -> None:
        super().__init__(body["id"])
        self._body = body
        self._client = client
        self.artist = body["primary_artist"]["name"]
        self.lyrics = lyrics if lyrics else ""
        self.primary_artist = Artist(client, body["primary_artist"])
        self.stats = Stats(body["stats"])
        self.album = Album(client, body["album"], []) if body.get("album") else None

        self.annotation_count = body["annotation_count"]
        self.api_path = body["api_path"]
        self.full_title = body["full_title"]
        self.header_image_thumbnail_url = body["header_image_thumbnail_url"]
        self.header_image_url = body["header_image_url"]
        self.lyrics_owner_id = body["lyrics_owner_id"]
        self.lyrics_state = body["lyrics_state"]
        self.path = body["path"]
        self.pyongs_count = body["pyongs_count"]
        self.song_art_image_thumbnail_url = body["song_art_image_thumbnail_url"]
        self.song_art_image_url = body["song_art_image_url"]
        self.title = body["title"]
        self.title_with_featured = body["title_with_featured"]
        self.url = body["url"]

    @property
    def _text_data(self) -> str:
        """Returns the text data for the song."""
        return self.lyrics

    def to_dict(self) -> dict[str, Any]:
        """Converts the Song object to a dictionary."""
        body = super().to_dict()
        body["artist"] = self.artist
        body["lyrics"] = self.lyrics
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
            filename = f"Lyrics_{self.artist.replace(' ', '')}_{self.title.replace(' ', '')}".lower()

        super().save_lyrics(
            filename=filename,
            extension=extension,
            overwrite=overwrite,
            ensure_ascii=ensure_ascii,
            sanitize=sanitize,
            verbose=verbose,
        )

    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else:
            lyr = self.lyrics[:100]
        return f'"{self.title}" by {self.artist}:\n    {lyr.replace("\n", "\n    ")}'

    def __cmp__(self, other):
        return (
            cmp(self.title, other.title)
            and cmp(self.artist, other.artist)
            and cmp(self.lyrics, other.lyrics)
        )
