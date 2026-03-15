import json
import os
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius
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
    )
    assert expected_filepath.is_file(), f"File not created at {expected_filepath}"

    content = expected_filepath.read_text()
    assert f'"name": "{album_object.name}"' in content, content
    assert f'"artist": "{album_object.artist["name"]}"' in content, content
    assert '"title": "Setup Serenade"' in content, content
    assert '"lyrics": "[Verse 1]\\nArrange the mocks' in content, content

    original_lyrics = album_object.tracks[0][1].lyrics
    album_object.tracks[0][1].lyrics = "Overwritten JSON Test"
    album_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
    )
    assert expected_filepath.is_file(), (
        f"Overwritten file not found at {expected_filepath}"
    )
    content_after_overwrite = expected_filepath.read_text()
    assert "Overwritten JSON Test" in content_after_overwrite, content_after_overwrite
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
    )
    assert expected_filepath.is_file(), f"File not created at {expected_filepath}"

    content = expected_filepath.read_text()
    assert "Track 1: Setup Serenade" in content, content
    assert "[Verse 1]\nArrange the mocks" in content, content
    assert "Track 2: Teardown Tango" in content, content
    assert "[Verse 1]\nReset the state" in content, content

    original_lyrics = album_object.tracks[0][1].lyrics
    album_object.tracks[0][1].lyrics = "Overwritten TXT Test"
    album_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
    )
    assert expected_filepath.is_file(), (
        f"Overwritten file not found at {expected_filepath}"
    )
    content_after_overwrite = expected_filepath.read_text()
    assert "Overwritten TXT Test" in content_after_overwrite, content_after_overwrite
    album_object.tracks[0][1].lyrics = original_lyrics


@pytest.fixture
def genius_client() -> Genius:
    return Genius("dummy_access_token", sleep_time=0)


def _make_search_all_response(album_data: dict[str, Any]) -> dict[str, Any]:
    hit = {"index": "album", "result": album_data}
    return {
        "sections": [
            {"type": "top_hits", "hits": [hit]},
            {"type": "album", "hits": [hit]},
        ]
    }


def _make_album_tracks_response(songs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "tracks": [{"song": s, "number": i + 1} for i, s in enumerate(songs)],
        "next_page": None,
    }


def test_fetch_lyrics_true_calls_lyrics(
    genius_client: Genius,
    mock_album_data: dict[str, Any],
    mock_track_data_list: list[dict[str, Any]],
) -> None:
    """When fetch_lyrics=True (default), lyrics() should be called for each track."""
    with (
        mock.patch.object(
            genius_client,
            "search_all",
            return_value=_make_search_all_response(mock_album_data),
        ),
        mock.patch.object(
            genius_client, "album", return_value={"album": mock_album_data}
        ),
        mock.patch.object(
            genius_client,
            "album_tracks",
            return_value=_make_album_tracks_response(mock_track_data_list),
        ),
        mock.patch.object(
            genius_client, "lyrics", return_value="some lyrics"
        ) as mock_lyrics,
    ):
        result = genius_client.search_album(
            name=mock_album_data["name"], fetch_lyrics=True
        )

    assert result is not None
    assert mock_lyrics.call_count == len(mock_track_data_list)
    for _, track in result.tracks:
        assert track.lyrics == "some lyrics"


def test_fetch_lyrics_false_skips_lyrics(
    genius_client: Genius,
    mock_album_data: dict[str, Any],
    mock_track_data_list: list[dict[str, Any]],
) -> None:
    """When fetch_lyrics=False, lyrics() is not called and tracks have empty lyrics."""
    with (
        mock.patch.object(
            genius_client,
            "search_all",
            return_value=_make_search_all_response(mock_album_data),
        ),
        mock.patch.object(
            genius_client, "album", return_value={"album": mock_album_data}
        ),
        mock.patch.object(
            genius_client,
            "album_tracks",
            return_value=_make_album_tracks_response(mock_track_data_list),
        ),
        mock.patch.object(
            genius_client, "lyrics", return_value="some lyrics"
        ) as mock_lyrics,
    ):
        result = genius_client.search_album(
            name=mock_album_data["name"], fetch_lyrics=False
        )

    assert result is not None
    assert mock_lyrics.call_count == 0
    for _, track in result.tracks:
        assert track.lyrics == ""
