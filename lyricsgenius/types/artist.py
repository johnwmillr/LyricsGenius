# LyricsGenius
# copyright 2025 John W. R. Miller
# See LICENSE for details.


from typing import TYPE_CHECKING, Any

from ..utils import safe_unicode
from .base import BaseEntity

if TYPE_CHECKING:
    from ..types.song import Song


class Artist(BaseEntity):
    """An artist with songs from Genius."""

    def __init__(self, body: dict[str, Any]) -> None:
        self._body = body
        self.songs: list[Song] = []

        self.api_path: str = body["api_path"]
        self.header_image_url: str = body["header_image_url"]
        self.image_url: str = body["image_url"]
        self.is_meme_verified: bool = body["is_meme_verified"]
        self.is_verified: bool = body["is_verified"]
        self.name: str = body["name"]
        self.url: str = body["url"]

    def __len__(self) -> int:
        return len(self.songs)

    @property
    def num_songs(self) -> int:
        return len(self)

    def add_song(
        self,
        new_song: Song,
        verbose: bool = True,
        include_features: bool = False,
    ) -> Song | None:
        """Adds a song to the Artist.

        This method adds a new song to the artist object. It checks
        if the song is already in artist's songs and whether the
        song's artist is the same as the `Artist` object.

        Args:
            new_song (:class:`Song <lyricsgenius.types.Song>`): Song to be added.
            verbose (:obj:`bool`, optional): prints operation result.
            include_features (:obj:`bool`, optional): If True, includes tracks
                featuring the artist.

        Returns:
            :obj:`Song`: Returns None on failure.

        Examples:
            .. code:: python

                genius = Genius(token)
                artist = genius.search_artist('Andy Shauf', max_songs=3)

                # Way 1
                song = genius.search_song('To You', artist.name)
                artist.add_song(song)
        """
        if new_song in self.songs:
            if verbose:
                print(
                    f"{safe_unicode(new_song.title)} already in {safe_unicode(self.name)}, not adding song."
                )
            return None
        if new_song.artist == self.name or (
            include_features and new_song.artist in new_song.featured_artists
        ):
            self.songs.append(new_song)
            return new_song
        if verbose:
            print(
                f"Can't add song by {safe_unicode(new_song.artist)}, artist must be {safe_unicode(self.name)}."
            )
        return None

    @property
    def _text_data(self) -> str:
        """Returns the text data for the artist."""
        return "\n\n".join(
            f"[Song {n}: {song.title}]\n{song.lyrics}"
            for n, song in enumerate(self.songs, start=1)
        ).strip()

    def to_dict(self) -> dict[str, Any]:
        body = super().to_dict()
        body["songs"] = [song.to_dict() for song in self.songs]
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
        """Return a string representation of the Artist object."""
        msg = f"{self.name}, {self.num_songs} songs"
        msg = msg[:-1] if self.num_songs == 1 else msg
        return msg

    def __repr__(self) -> str:
        """Return a string representation of the Artist object."""
        return f"Artist(name={self.name}, num_songs={self.num_songs})"

    def __eq__(self, other: object) -> bool:
        """Check if two Artist objects are equal."""
        if not isinstance(other, Artist):
            return False
        if self._body.get("id", 1) == other._body.get("id", -1):
            return True
        if self.name != other.name or len(self.songs) != len(other.songs):
            return False
        return sorted(self.songs, key=lambda s: s.title) == sorted(
            other.songs, key=lambda s: s.title
        )
