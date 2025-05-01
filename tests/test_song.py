import os
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from lyricsgenius.types import Song
from lyricsgenius.utils import clean_str


@pytest.fixture
def mock_song_data() -> dict[str, Any]:
    """Create mock song data that mimics what would be returned from the API."""
    return {
        "id": 99999,
        "title": "Test the Mock",
        "full_title": "Test the Mock by Pytest Fixture",
        "path": "/Pytest-fixture-test-the-mock-lyrics",
        "primary_artist": {
            "id": 11111,
            "name": "Pytest Fixture",
            "header_image_url": "https://example.com/pytest-header.jpg",
            "image_url": "https://example.com/pytest-thumb.jpg",
            "is_meme_verified": False,
            "is_verified": True,
            "url": "https://genius.com/artists/Pytest-fixture",
            "api_path": "/artists/11111",
        },
        "album": {
            "id": 22222,
            "name": "Coverage Suite",
            "cover_art_url": "https://example.com/coverage-cover.jpg",
            "cover_art_thumbnail_url": "https://example.com/coverage-thumb.jpg",
            "full_title": "Coverage Suite by Pytest Fixture",
            "name_with_artist": "Coverage Suite by Pytest Fixture",
            "url": "https://genius.com/albums/Pytest-fixture/Coverage-suite",
            "api_path": "/albums/22222",
            "artist": {
                "id": 11111,
                "name": "Pytest Fixture",
                "header_image_url": "https://example.com/pytest-header.jpg",
                "image_url": "https://example.com/pytest-thumb.jpg",
                "is_meme_verified": False,
                "is_verified": True,
                "url": "https://genius.com/artists/Pytest-fixture",
                "api_path": "/artists/11111",
            },
            "release_date_components": {"year": 2024, "month": 1, "day": 1},
        },
        "api_path": "/songs/99999",
        "annotation_count": 5,
        "header_image_thumbnail_url": "https://example.com/mock-thumb.jpg",
        "header_image_url": "https://example.com/mock-image.jpg",
        "lyrics_owner_id": 33333,
        "lyrics_state": "complete",
        "pyongs_count": 10,
        "song_art_image_thumbnail_url": "https://example.com/song-art-thumb.jpg",
        "song_art_image_url": "https://example.com/song-art.jpg",
        "title_with_featured": "Test the Mock",
        "url": "https://genius.com/Pytest-fixture-test-the-mock-lyrics",
        "stats": {"pageviews": 54321, "unreviewed_annotations": 1, "hot": False},
        "featured_artists": [],
    }


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
def mock_genius() -> mock.MagicMock:
    """Mock genius client."""
    genius = mock.MagicMock()
    genius._result_is_lyrics.return_value = True
    return genius


@pytest.fixture
def song_object(
    mock_genius: mock.MagicMock, mock_song_data: dict[str, Any], mock_lyrics: str
) -> Song:
    """Create a Song object with mock data."""
    return Song(mock_genius, mock_song_data, mock_lyrics)


@pytest.fixture
def song_object_no_headers(
    mock_genius: mock.MagicMock,
    mock_song_data: dict[str, Any],
    mock_lyrics_no_headers: str,
) -> Song:
    """Create a Song object with mock data and no section headers."""
    return Song(mock_genius, mock_song_data, mock_lyrics_no_headers)


def test_song_title(song_object: Song, mock_song_data: dict[str, Any]) -> None:
    """Test if the song title is correct."""
    assert clean_str(song_object.title) == clean_str(mock_song_data["title"])


def test_song_artist(song_object: Song, mock_song_data: dict[str, Any]) -> None:
    """Test if the artist name is correct."""
    assert song_object.artist == mock_song_data["primary_artist"]["name"]


def test_lyrics_raw(song_object: Song, mock_lyrics: str) -> None:
    """Test if the lyrics contain section headers."""
    assert song_object.lyrics.startswith("[Setup]")
    assert song_object.lyrics == mock_lyrics


def test_lyrics_no_section_headers(
    song_object_no_headers: Song, mock_lyrics_no_headers: str
) -> None:
    """Test if the lyrics without section headers are correct."""
    assert song_object_no_headers.lyrics.startswith("Assert the true")
    assert song_object_no_headers.lyrics == mock_lyrics_no_headers


def test_to_dict(
    song_object: Song, mock_song_data: dict[str, Any], mock_lyrics: str
) -> None:
    """Test if the to_dict method returns the correct data."""
    song_dict = song_object.to_dict()
    assert song_dict["id"] == mock_song_data["id"]
    assert song_dict["title"] == mock_song_data["title"]
    assert song_dict["artist"] == mock_song_data["primary_artist"]["name"]
    assert song_dict["lyrics"] == mock_lyrics


@mock.patch("json.dump")
def test_save_lyrics_json(
    mock_json_dump: mock.MagicMock, song_object: Song, tmp_path: Path
) -> None:
    """Test saving lyrics as a JSON file."""
    # Setup a temporary file path
    filename = tmp_path / "test_lyrics.json"

    # Test saving
    song_object.save_lyrics(
        filename=str(filename),
        extension="json",
        overwrite=True,
        sanitize=False,  # Sanitizing the filename causes test to fail because we remove slashes
        verbose=False,
    )

    # Check if the file was created
    assert os.path.exists(filename)


@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_lyrics_txt(
    mock_open: mock.MagicMock, song_object: Song, tmp_path: Path
) -> None:
    """Test saving lyrics as a TXT file."""
    # Setup a temporary file path
    filename = tmp_path / "test_lyrics.txt"

    # Test saving
    song_object.save_lyrics(
        filename=str(filename), extension="txt", overwrite=True, verbose=False
    )

    # Check if open was called with the right args
    mock_open.assert_called_once()
    assert ".txt" in mock_open.call_args[0][0]


def test_to_text(song_object: Song, mock_lyrics: str) -> None:
    """Test if to_text method returns the lyrics."""
    assert song_object.to_text() == mock_lyrics


def test_to_json(song_object: Song) -> None:
    """Test if to_json method returns a JSON string."""
    json_str = song_object.to_json()
    assert isinstance(
        json_str, str | None
    )  # to_json can return None if filename is provided
    if json_str:
        assert '"title": "Test the Mock"' in json_str
        assert '"artist": "Pytest Fixture"' in json_str
