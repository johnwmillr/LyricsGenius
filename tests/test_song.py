import json
import os
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from lyricsgenius.types import Song
from lyricsgenius.utils import clean_str


@pytest.fixture
def mock_song_data() -> dict[str, Any]:
    """Returns 'Mocking the Tests' from song_info_mocked.json as a dict."""
    with open("tests/fixtures/song_info_mocked.json", "r") as f:
        return next(song for song in json.load(f) if song["id"] == 42424242)


@pytest.fixture
def mock_lyrics() -> str:
    """Create mock lyrics for testing."""
    return (
        "[Setup]\n"
        "Assert the true, mock the new\n"
        "Patch the world, see it through\n"
        "Arrange the state, don't delay\n"
        "\n"
        "[Act]\n"
        "Call the function, watch it run\n"
        "Did it break? Was it fun?\n"
        "Capture output, every byte\n"
        "\n"
        "[Assert]\n"
        "Check the value, is it right?\n"
        "Compare the strings, day and night\n"
        "Test complete, green light bright"
    )


@pytest.fixture
def mock_lyrics_no_headers() -> str:
    """Create mock lyrics without section headers."""
    return (
        "Assert the true, mock the new\n"
        "Patch the world, see it through\n"
        "Arrange the state, don't delay\n"
        "\n"
        "Call the function, watch it run\n"
        "Did it break? Was it fun?\n"
        "Capture output, every byte\n"
        "\n"
        "Check the value, is it right?\n"
        "Compare the strings, day and night\n"
        "Test complete, green light bright"
    )


@pytest.fixture
def song_object(mock_song_data: dict[str, Any], mock_lyrics: str) -> Song:
    """Create a Song object with mock data."""
    return Song(mock_lyrics, mock_song_data)


@pytest.fixture
def song_object_no_headers(
    mock_song_data: dict[str, Any],
    mock_lyrics_no_headers: str,
) -> Song:
    """Create a Song object with mock data and no section headers."""
    return Song(mock_lyrics_no_headers, mock_song_data)


def test_song_title(song_object: Song, mock_song_data: dict[str, Any]) -> None:
    """Test if the song title is correct."""
    assert song_object.title == mock_song_data["title"]


def test_song_artist(song_object: Song, mock_song_data: dict[str, Any]) -> None:
    """Test if the artist name is correct."""
    assert song_object.artist == mock_song_data["primary_artist"]["name"]


def test_song_primary_artists(
    song_object: Song, mock_song_data: dict[str, Any]
) -> None:
    """Test if primary_artists is populated correctly."""
    assert song_object.primary_artists == mock_song_data["primary_artists"]
    assert song_object.primary_artists[0]["name"] == "Py Testerson"


def test_song_writer_artists(song_object: Song, mock_song_data: dict[str, Any]) -> None:
    """Test if writer_artists is populated correctly."""
    assert song_object.writer_artists == mock_song_data["writer_artists"]
    assert song_object.writer_artists[0]["name"] == "Test Writer"


def test_song_producer_artists(
    song_object: Song, mock_song_data: dict[str, Any]
) -> None:
    """Test if producer_artists is populated correctly."""
    assert song_object.producer_artists == mock_song_data["producer_artists"]
    assert song_object.producer_artists[0]["name"] == "Test Producer"


def test_song_featured_artists(
    song_object: Song, mock_song_data: dict[str, Any]
) -> None:
    """Test if featured_artists is populated correctly."""
    assert song_object.featured_artists == mock_song_data["featured_artists"]
    assert song_object.featured_artists[0]["name"] == "Mock Feature"


def test_song_artist_fields_default_empty(
    mock_song_data: dict[str, Any], mock_lyrics: str
) -> None:
    """Test that artist list fields default to empty lists when absent from body."""
    body = {
        k: v
        for k, v in mock_song_data.items()
        if k
        not in (
            "primary_artists",
            "writer_artists",
            "producer_artists",
            "featured_artists",
        )
    }
    song = Song(mock_lyrics, body)
    assert song.primary_artists == []
    assert song.writer_artists == []
    assert song.producer_artists == []
    assert song.featured_artists == []


def test_to_dict(
    song_object: Song, mock_song_data: dict[str, Any], mock_lyrics: str
) -> None:
    """Test if the to_dict method returns the correct data."""
    song_dict = song_object.to_dict()
    assert song_dict["id"] == mock_song_data["id"]
    assert song_dict["title"] == mock_song_data["title"]
    assert song_dict["artist"] == mock_song_data["primary_artist"]["name"]
    assert song_dict["lyrics"] == mock_lyrics


def test_to_json(song_object: Song) -> None:
    """Test if to_json method returns a JSON string."""
    json_str = song_object.to_json()
    assert isinstance(json_str, str), json_str
    assert '"title": "Mocking the Tests"' in json_str
    assert '"artist": "Py Testerson"' in json_str


def test_to_text(song_object: Song, mock_lyrics: str) -> None:
    """Test if to_text method returns the lyrics."""
    assert song_object.to_text() == mock_lyrics


def test_save_lyrics_json(song_object: Song, tmp_path: Path) -> None:
    """Test saving lyrics as a JSON file."""
    filename = tmp_path / "test_lyrics.json"
    song_object.save_lyrics(
        filename=str(filename),
        extension="json",
        overwrite=True,
    )

    # Check that the file was written correctly
    assert filename.is_file(), filename
    json_str = filename.read_text()
    assert '"title": "Mocking the Tests"' in json_str, json_str
    assert '"artist": "Py Testerson"' in json_str, json_str


def test_save_lyrics_txt(song_object: Song, tmp_path: Path) -> None:
    """Test saving lyrics as a TXT file."""
    filename = tmp_path / "test_lyrics.txt"
    song_object.save_lyrics(
        filename=str(filename),
        extension="txt",
        overwrite=True,
    )

    # Check that the file was written correctly
    assert filename.is_file(), filename
    assert filename.read_text() == song_object.lyrics, filename


def test_save_lyrics_with_path_json(song_object: Song, tmp_path: Path) -> None:
    """Test that save_lyrics creates the directory when a path is included in filename."""
    output_dir = tmp_path / "output" / "nested"
    song_object.save_lyrics(
        filename=str(output_dir / "test_song"),
        extension="json",
        overwrite=True,
    )

    saved_file = output_dir / "test_song.json"
    assert saved_file.is_file(), f"Expected file at {saved_file}"
    content = saved_file.read_text()
    assert '"title": "Mocking the Tests"' in content, content
    assert '"artist": "Py Testerson"' in content, content


def test_save_lyrics_with_path_txt(song_object: Song, tmp_path: Path) -> None:
    """Test that save_lyrics creates the directory when a path is included in filename."""
    output_dir = tmp_path / "lyrics_output"
    song_object.save_lyrics(
        filename=str(output_dir / "test_song"),
        extension="txt",
        overwrite=True,
    )

    saved_file = output_dir / "test_song.txt"
    assert saved_file.is_file(), f"Expected file at {saved_file}"
    assert saved_file.read_text() == song_object.lyrics


def test_save_lyrics_path_creates_directory(song_object: Song, tmp_path: Path) -> None:
    """Test that save_lyrics creates the parent directory if it doesn't exist."""
    new_dir = tmp_path / "brand_new_dir"
    assert not new_dir.exists()

    song_object.save_lyrics(
        filename=str(new_dir / "out"),
        extension="json",
        overwrite=True,
    )

    assert new_dir.is_dir()
    assert (new_dir / "out.json").is_file()
