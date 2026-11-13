"""Tests for the Artist type: adding and finding songs, and its output."""

import json
from pathlib import Path
from typing import Any

import pytest

from lyricsgenius.types import Artist, Song

ARTIST_NAME = "Pytest Fixture"


def _artist_data(id_: int = 1001, name: str = ARTIST_NAME) -> dict[str, Any]:
    """Builds the data for an invented artist."""
    return {
        "id": id_,
        "name": name,
        "url": f"https://genius.com/artists/{name.replace(' ', '-')}",
        "api_path": f"/artists/{id_}",
        "header_image_url": "https://example.com/header.jpg",
        "image_url": "https://example.com/image.jpg",
        "is_meme_verified": False,
        "is_verified": True,
    }


def _song(
    id_: int, title: str, artist: str = ARTIST_NAME, featured: list[str] | None = None
) -> Song:
    """Builds a Song with invented lyrics."""
    body = {
        "id": id_,
        "title": title,
        "primary_artist": {"name": artist},
        "featured_artists": [{"name": name} for name in featured or []],
    }
    return Song(f"[Verse 1]\nLyrics of {title}", body)


@pytest.fixture
def artist() -> Artist:
    """Provides an Artist with two songs."""
    artist = Artist(_artist_data())
    artist.songs = [_song(1, "Assert Equals Blues"), _song(2, "Patch Decorator Funk")]
    return artist


def test_artist_add_song_accepts_songs_by_the_artist(artist: Artist) -> None:
    """A song by the artist is added and returned."""
    song = _song(3, "Refactor Rhapsody")

    assert artist.add_song(song) is song
    assert artist.songs[-1] is song


def test_artist_add_song_rejects_songs_by_other_artists(artist: Artist) -> None:
    """A song by another artist isn't added."""
    assert artist.add_song(_song(3, "Side Effect Ballad", artist="Mock Runner")) is None
    assert artist.num_songs == 2


def test_artist_add_song_rejects_duplicates(artist: Artist) -> None:
    """A song already in the artist's songs isn't added twice."""
    assert artist.add_song(_song(1, "Assert Equals Blues")) is None
    assert artist.num_songs == 2


@pytest.mark.parametrize(
    ("include_features", "added"),
    [
        pytest.param(True, True, id="included"),
        pytest.param(False, False, id="excluded"),
    ],
)
def test_artist_add_song_takes_features_only_when_asked(
    artist: Artist, include_features: bool, added: bool
) -> None:
    """A song only featuring the artist is added only with include_features."""
    song = _song(
        3, "Integration Test Jam", artist="Mock Runner", featured=[ARTIST_NAME]
    )

    artist.add_song(song, include_features=include_features)

    assert (song in artist.songs) is added


@pytest.mark.parametrize(
    ("kwargs", "title"),
    [
        pytest.param({"song_id": 2}, "Patch Decorator Funk", id="by_id"),
        pytest.param({"song_id": 99}, None, id="missing_id"),
    ],
)
def test_artist_get_song_finds_song(
    artist: Artist, kwargs: dict[str, Any], title: str | None
) -> None:
    """A song is found by its ID, or None is returned."""
    song = artist.get_song(**kwargs)

    assert (song.title if song else None) == title


def test_artist_to_text_numbers_each_song(artist: Artist) -> None:
    """The text form gives each song's number, title and lyrics."""
    assert artist.to_text() == (
        "[Song 1: Assert Equals Blues]\n[Verse 1]\nLyrics of Assert Equals Blues\n\n"
        "[Song 2: Patch Decorator Funk]\n[Verse 1]\nLyrics of Patch Decorator Funk"
    )


def test_artist_to_dict_includes_songs(artist: Artist) -> None:
    """The dict form holds the artist data and each song's dict form."""
    artist_dict = artist.to_dict()

    assert artist_dict["name"] == ARTIST_NAME
    assert artist_dict["songs"] == [song.to_dict() for song in artist.songs]


@pytest.mark.parametrize(
    ("num_songs", "text"),
    [
        pytest.param(1, f"{ARTIST_NAME}, 1 song", id="one"),
        pytest.param(2, f"{ARTIST_NAME}, 2 songs", id="several"),
    ],
)
def test_artist_str_counts_songs(artist: Artist, num_songs: int, text: str) -> None:
    """The string form gives the name and the number of songs."""
    artist.songs = artist.songs[:num_songs]

    assert str(artist) == text


@pytest.mark.parametrize("extension", ["json", "txt"])
def test_artist_save_lyrics_writes_serialized_artist(
    artist: Artist, tmp_path: Path, extension: str
) -> None:
    """Saving writes the artist's JSON or text form to the file."""
    path = tmp_path / f"artist.{extension}"

    artist.save_lyrics(filename=str(tmp_path / "artist"), extension=extension)

    if extension == "json":
        assert json.loads(path.read_text()) == artist.to_dict()
    else:
        assert path.read_text() == artist.to_text()


def test_artist_save_lyrics_default_filename_uses_name_and_song_count(
    artist: Artist, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without a filename, the file is named after the artist and song count."""
    monkeypatch.chdir(tmp_path)

    artist.save_lyrics()

    assert [path.name for path in tmp_path.iterdir()] == [
        "saved_artist_lyrics_pytest_fixture_2_songs.json"
    ]
