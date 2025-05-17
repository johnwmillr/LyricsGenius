from typing import Any

from ..utils import convert_to_datetime
from .base import BaseEntity
from .song import Song  # Import Song class


class Album(BaseEntity):
    """An album from Genius."""

    def __init__(self, body: dict[str, Any], songs: list[Song]) -> None:
        """
        Initialize an Album object.

        Args:
            body (dict[str, Any]): Album metadata.
            songs (list[Song]): A list of Song objects for the album.
        """
        self._body = body
        self.artist: dict[str, Any] = body["artist"]

        # Store tracks as a list of tuples: (inferred_track_number, Song_object)
        self.tracks: list[tuple[int, Song]] = []
        for i, song_obj in enumerate(songs):
            # Infer track number from the order in the list (1-based index)
            self.tracks.append((i + 1, song_obj))

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
            f"[Track {track_num}: {song_obj.title}]\n{song_obj.lyrics}"
            for track_num, song_obj in self.tracks
        ).strip()

    def to_dict(self) -> dict[str, Any]:
        body = super().to_dict()
        body["artist"] = self.artist["name"]

        # Serialize tracks: create a list of dictionaries, each representing a track
        # with its number and the song data.
        serialized_tracks = []
        for track_num, song_obj in self.tracks:
            serialized_tracks.append(
                {
                    "number": track_num,
                    "song": song_obj.to_dict(),
                }
            )
        body["tracks"] = serialized_tracks

        # Add release date string if components exist
        if self.release_date_components:
            body["release_date"] = self.release_date_components.strftime("%Y-%m-%d")
        else:
            body["release_date"] = None
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

    def __str__(self) -> str:
        """Return a string representation of the Album object."""
        return f'"{self.name}" by {self.artist["name"]}, {len(self.tracks)} tracks'

    def __repr__(self) -> str:
        """Return a string representation of the Album object."""
        return f"Album(name='{self.name}', artist='{self.artist['name']}')"

    def __eq__(self, other: object) -> bool:
        """Check if two Album objects are equal."""
        if not isinstance(other, Album):
            return False
        if self._body.get("id", 1) == other._body.get("id", -1):
            return True

        return (
            self.name == other.name
            and self.artist["id"] == other.artist["id"]
            and self.tracks == other.tracks
        )
