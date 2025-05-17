# LyricsGenius
# copyright 2025 John W. R. Miller
# See LICENSE for details.

from typing import Any

from .base import BaseEntity


class Song(BaseEntity):
    """Lyrics and metadata for a song from Genius."""

    def __init__(self, lyrics: str, body: dict[str, Any]) -> None:
        """
        Initialize a Song object with lyrics and song metadata.

        Args:
            lyrics (str): The lyrics of the song.
            body (dict[str, Any]): A dictionary containing song metadata.
        """
        self.lyrics = lyrics
        self._body = body

        self.artist: str = body["primary_artist"]["name"]
        self.primary_artist: dict[str, Any] = body["primary_artist"]
        self.album: dict[str, Any] | None = body.get("album")
        self.annotation_count: int | None = body.get("annotation_count")
        self.api_path: str | None = body.get("api_path")
        self.full_title: str | None = body.get("full_title")
        self.header_image_thumbnail_url: str | None = body.get(
            "header_image_thumbnail_url"
        )
        self.header_image_url: str | None = body.get("header_image_url")
        self.lyrics_owner_id: int | None = body.get("lyrics_owner_id")
        self.lyrics_state: str | None = body.get("lyrics_state")
        self.path: str | None = body.get("path")
        self.pyongs_count: int | None = body.get("pyongs_count")
        self.song_art_image_thumbnail_url: str | None = body.get(
            "song_art_image_thumbnail_url"
        )
        self.song_art_image_url: str | None = body.get("song_art_image_url")
        self.title: str = body["title"]
        self.title_with_featured: str | None = body.get("title_with_featured")
        self.url: str | None = body.get("url")
        self.featured_artists: list[dict[str, Any]] = body.get("featured_artists", [])

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

    def __str__(self) -> str:
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else:
            lyr = self.lyrics[:100]
        return f'"{self.title}" by {self.artist}:\n    {lyr.replace("\n", "\n    ")}'

    def __repr__(self) -> str:
        """Return a string representation of the Song object."""
        return f"Song(title={self.title}, artist={self.artist})"

    def __eq__(self, other: object) -> bool:
        """Check if two Song objects are equal."""
        if not isinstance(other, Song):
            return False
        if self._body.get("id", 1) == other._body.get("id", -1):
            return True

        # Fallback to attribute comparison if IDs are not definitive
        return (
            self.title == other.title
            and self.artist == other.artist
            and self.lyrics == other.lyrics
        )
