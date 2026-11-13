"""Tests for the Song type: its fields, serialization and saving to disk."""

import json
from pathlib import Path
from typing import Any

import pytest

from lyricsgenius.types import Song

LYRICS = (
    "[Setup]\n"
    "Assert the true, mock the new\n"
    "Patch the world, see it through\n"
    "\n"
    "[Act]\n"
    "Call the function, watch it run"
)
ARTIST_LISTS = (
    "primary_artists",
    "writer_artists",
    "producer_artists",
    "featured_artists",
)


@pytest.fixture
def song_data() -> dict[str, Any]:
    """Provides the data for the invented song "Mocking the Tests"."""
    songs = json.loads(Path("tests/fixtures/song_info_mocked.json").read_text())
    return next(song for song in songs if song["id"] == 42424242)


@pytest.fixture
def song(song_data: dict[str, Any]) -> Song:
    """Provides a Song built from the invented data and lyrics."""
    return Song(LYRICS, song_data)


def test_song_reads_artist_from_primary_artist(song: Song) -> None:
    """The artist is the primary artist's name."""
    assert song.artist == "Py Testerson"


def test_song_artist_lists_default_to_empty(song_data: dict[str, Any]) -> None:
    """Artist lists missing from the song data default to empty lists."""
    body = {k: v for k, v in song_data.items() if k not in ARTIST_LISTS}

    song = Song(LYRICS, body)

    assert [getattr(song, name) for name in ARTIST_LISTS] == [[], [], [], []]


def test_song_to_dict_adds_artist_and_lyrics(
    song: Song, song_data: dict[str, Any]
) -> None:
    """The dict form is the song data plus its artist name and lyrics."""
    assert song.to_dict() == {**song_data, "artist": "Py Testerson", "lyrics": LYRICS}


def test_song_to_json_serializes_dict_form(song: Song) -> None:
    """The JSON form encodes the dict form."""
    json_str = song.to_json()

    assert json_str is not None
    assert json.loads(json_str) == song.to_dict()


def test_song_to_text_returns_lyrics(song: Song) -> None:
    """The text form is the lyrics."""
    assert song.to_text() == LYRICS


@pytest.mark.parametrize("extension", ["json", "txt"])
@pytest.mark.parametrize("directory", ["", "output/nested"], ids=["flat", "nested"])
def test_song_save_lyrics_writes_serialized_song(
    song: Song, tmp_path: Path, extension: str, directory: str
) -> None:
    """Saving writes the JSON or text form, creating missing directories."""
    path = tmp_path / directory / f"song.{extension}"

    song.save_lyrics(filename=str(tmp_path / directory / "song"), extension=extension)

    if extension == "json":
        assert json.loads(path.read_text()) == song.to_dict()
    else:
        assert path.read_text() == LYRICS


def test_song_save_lyrics_rejects_other_formats(song: Song, tmp_path: Path) -> None:
    """Only JSON and text files can be saved."""
    with pytest.raises(AssertionError, match="JSON or TXT"):
        song.save_lyrics(filename=str(tmp_path / "song"), extension="csv")


@pytest.mark.parametrize(
    ("answer", "replaced"),
    [
        pytest.param("y", True, id="yes"),
        pytest.param("n", False, id="no"),
    ],
)
def test_song_save_lyrics_asks_before_overwriting(
    song: Song,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    answer: str,
    replaced: bool,
) -> None:
    """An existing file is replaced only if the user agrees."""
    path = tmp_path / "song.txt"
    path.write_text("old")
    prompts: list[str] = []

    def _answer(prompt: str) -> str:
        prompts.append(prompt)
        return answer

    monkeypatch.setattr("builtins.input", _answer)

    song.save_lyrics(filename=str(tmp_path / "song"), extension="txt")

    assert len(prompts) == 1
    assert path.read_text() == (LYRICS if replaced else "old")


def test_song_save_lyrics_overwrites_without_asking_when_told(
    song: Song, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """With overwrite=True, an existing file is replaced without a prompt."""
    path = tmp_path / "song.txt"
    path.write_text("old")
    monkeypatch.setattr("builtins.input", pytest.fail)

    song.save_lyrics(filename=str(tmp_path / "song"), extension="txt", overwrite=True)

    assert path.read_text() == LYRICS


@pytest.mark.parametrize(
    ("ensure_ascii", "expected"),
    [
        pytest.param(True, '"Beyonc\\u00e9"', id="escaped"),
        pytest.param(False, '"Beyoncé"', id="kept"),
    ],
)
def test_song_save_lyrics_honors_ensure_ascii(
    song_data: dict[str, Any], tmp_path: Path, ensure_ascii: bool, expected: str
) -> None:
    """Non-ASCII characters are escaped in the JSON file unless told otherwise."""
    song = Song(LYRICS, {**song_data, "title": "Beyoncé"})

    song.save_lyrics(filename=str(tmp_path / "song"), ensure_ascii=ensure_ascii)

    assert expected in (tmp_path / "song.json").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("sanitize", "name"),
    [
        pytest.param(True, "What's up.txt", id="sanitized"),
        pytest.param(False, "What's up?.txt", id="kept"),
    ],
)
def test_song_save_lyrics_sanitizes_filename(
    song: Song, tmp_path: Path, sanitize: bool, name: str
) -> None:
    """Characters invalid in filenames are removed from the name unless told not to."""
    song.save_lyrics(
        filename=str(tmp_path / "What's up?"), extension="txt", sanitize=sanitize
    )

    assert [path.name for path in tmp_path.iterdir()] == [name]


def test_song_save_lyrics_default_filename_uses_artist_and_title(
    song: Song, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without a filename, the file is named after the artist and title."""
    monkeypatch.chdir(tmp_path)

    song.save_lyrics()

    assert [path.name for path in tmp_path.iterdir()] == [
        "saved_song_lyrics_py_testerson_mocking_the_tests.json"
    ]
