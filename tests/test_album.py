import json
import os
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from lyricsgenius.types import Album, Artist, Song
from lyricsgenius.utils import sanitize_filename


@pytest.fixture
def mock_album_data() -> dict[str, Any]:
    """Return the contents of album_info_mocked.json as a dict."""
    with open("tests/fixtures/album_info_mocked.json", "r") as f:
        return json.load(f)


@pytest.fixture
def mock_album_artist_data(mock_album_data: dict[str, Any]) -> dict[str, Any]:
    """Mock data for the album's artist."""
    return mock_album_data["artist"]


@pytest.fixture
def mock_track_data_list() -> list[dict[str, Any]]:
    """Load mock track data from song_info_mocked.json (first two songs)."""
    with open("tests/fixtures/song_info_mocked.json", "r") as f:
        songs = json.load(f)
    return songs[:2]


@pytest.fixture
def mock_track_lyrics_list() -> list[str]:
    """Mock lyrics for the tracks."""
    return [
        "[Verse 1]\nArrange the mocks, prepare the scene,\nBefore the test, keep it clean.",
        "[Verse 1]\nReset the state, undo the change,\nAfter the test, rearrange.",
    ]


@pytest.fixture
def mock_track_objects(
    mock_track_lyrics_list: list[str], mock_track_data_list: list[dict[str, Any]]
) -> list[Song]:
    """Creates a list of mock Song objects for the album tracks."""
    songs: list[Song] = []
    for lyrics, data in zip(mock_track_lyrics_list, mock_track_data_list, strict=True):
        songs.append(Song(lyrics, data))
    return songs


@pytest.fixture
def album_object(
    mock_album_data: dict[str, Any], mock_track_objects: list[Song]
) -> Album:
    """Creates the Album object populated with mock tracks."""
    return Album(mock_album_data, mock_track_objects)


def test_album_instance(album_object: Album) -> None:
    """Test if the created object is an Album instance."""
    assert isinstance(album_object, Album)


def test_album_name(album_object: Album, mock_album_data: dict[str, Any]) -> None:
    """Test if the album name is correct."""
    assert album_object.name == mock_album_data["name"]


def test_album_artist(
    album_object: Album, mock_album_artist_data: dict[str, Any]
) -> None:
    """Test if the album artist name is correct."""
    assert album_object.artist["name"] == mock_album_artist_data["name"]
    assert album_object.artist["id"] == mock_album_artist_data["id"]


def test_tracks_populated(album_object: Album, mock_track_objects: list[Song]) -> None:
    """Test if the tracks list is populated correctly."""
    assert len(album_object.tracks) == len(mock_track_objects)
    assert album_object.tracks[0][1].title == mock_track_objects[0].title
    assert album_object.tracks[1][1].title == mock_track_objects[1].title


def test_get_track_by_position(
    album_object: Album, mock_track_objects: list[Song]
) -> None:
    """Test retrieving a track by its position (1-based index)."""
    # Find track by iterating and checking track.number
    target_position_1 = 1
    found_track_1 = None
    for number, song in album_object.tracks:
        if number == target_position_1:
            found_track_1 = song  # The test expects a Song object
            break
    assert found_track_1 is not None
    assert found_track_1.title == mock_track_objects[0].title

    target_position_2 = 2
    found_track_2 = None
    for number, song in album_object.tracks:
        if number == target_position_2:
            found_track_2 = song
            break
    assert found_track_2 is not None
    assert found_track_2.title == mock_track_objects[1].title

    # Test invalid positions (0 and out of bounds)
    target_position_0 = 0
    found_track_0 = None
    for number, song in album_object.tracks:
        if number == target_position_0:
            found_track_0 = song
            break
    assert found_track_0 is None

    target_position_invalid = len(mock_track_objects) + 1
    found_track_invalid = None
    for number, song in album_object.tracks:
        if number == target_position_invalid:
            found_track_invalid = song
            break
    assert found_track_invalid is None


def test_to_dict(
    album_object: Album, mock_album_data: dict[str, Any], mock_track_objects: list[Song]
) -> None:
    """Test the to_dict method."""
    album_dict = album_object.to_dict()
    assert album_dict["name"] == mock_album_data["name"]
    assert album_dict["artist"] == mock_album_data["artist"]["name"]
    assert "release_date" in album_dict
    assert isinstance(album_dict["release_date"], str)
    assert len(album_dict["tracks"]) == len(mock_track_objects)
    assert album_dict["tracks"][0]["song"]["title"] == mock_track_objects[0].title
    assert "lyrics" in album_dict["tracks"][0]["song"]


def test_saving_json_file(album_object: Album, tmp_path: Path) -> None:
    extension = "json"
    filename_base = "Lyrics_" + album_object.name.replace(" ", "")
    sanitized_base = sanitize_filename(filename_base)
    expected_filepath = tmp_path / f"{sanitized_base}.{extension}"

    album_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file(), f"File not created at {expected_filepath}"

    content = expected_filepath.read_text()
    assert f'"name": "{album_object.name}"' in content
    assert f'"artist": "{album_object.artist["name"]}"' in content
    assert '"title": "Setup Serenade"' in content
    assert '"lyrics": "[Verse 1]\\nArrange the mocks' in content

    original_lyrics = album_object.tracks[0][1].lyrics
    album_object.tracks[0][1].lyrics = "Overwritten JSON Test"
    album_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file()
    content_after_overwrite = expected_filepath.read_text()
    assert "Overwritten JSON Test" in content_after_overwrite
    album_object.tracks[0][1].lyrics = original_lyrics


def test_saving_txt_file(album_object: Album, tmp_path: Path) -> None:
    extension = "txt"
    filename_base = "Lyrics_" + album_object.name.replace(" ", "")
    sanitized_base = sanitize_filename(filename_base)
    expected_filepath = tmp_path / f"{sanitized_base}.{extension}"

    album_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file(), f"File not created at {expected_filepath}"

    content = expected_filepath.read_text()
    assert "Track 1: Setup Serenade" in content
    assert "[Verse 1]\nArrange the mocks" in content
    assert "Track 2: Teardown Tango" in content
    assert "[Verse 1]\nReset the state" in content

    original_lyrics = album_object.tracks[0][1].lyrics
    album_object.tracks[0][1].lyrics = "Overwritten TXT Test"
    album_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file()
    content_after_overwrite = expected_filepath.read_text()
    assert "Overwritten TXT Test" in content_after_overwrite
    album_object.tracks[0][1].lyrics = original_lyrics
