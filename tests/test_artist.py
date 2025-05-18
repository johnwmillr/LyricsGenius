import json
import os
from pathlib import Path  # For tmp_path
from typing import Any
from unittest import mock

import pytest

from lyricsgenius.types import Artist, Song
from lyricsgenius.utils import sanitize_filename


@pytest.fixture
def mock_genius_client() -> mock.MagicMock:
    """Provides a mock Genius client instance."""
    client = mock.MagicMock()
    client.verbose = False
    # Mock methods used by Artist/Song if necessary
    client._result_is_lyrics = mock.MagicMock(return_value=True)
    client.lyrics = mock.MagicMock(return_value="Mocked Lyrics")  # Placeholder
    client.song = mock.MagicMock(return_value={"song": {}})  # Placeholder
    return client


@pytest.fixture
def mock_artist_data() -> dict[str, Any]:
    """Return the contents of artist_info_mocked.json as a dict."""
    with open("tests/fixtures/artist_info_mocked.json", "r") as f:
        return json.load(f)


@pytest.fixture
def mock_primary_artist_data() -> dict[str, Any]:
    """Mock data for the primary test artist."""
    return {
        "id": 1001,
        "name": "Pytest Fixture",
        "url": "https://genius.com/artists/Pytest-fixture",
        "api_path": "/artists/1001",
        "header_image_url": "https://example.com/pytest_header.jpg",
        "image_url": "https://example.com/pytest.jpg",
        "is_meme_verified": False,
        "is_verified": True,
    }


@pytest.fixture
def mock_primary_songs_data(
    mock_primary_artist_data: dict[str, Any],
) -> list[dict[str, Any]]:
    """Mock data for the primary artist's songs, matching test_song.py structure."""
    song1 = {
        "id": 10101,
        "title": "Assert Equals Blues",
        "full_title": "Assert Equals Blues by Pytest Fixture",
        "path": "/Pytest-fixture-assert-equals-blues-lyrics",
        "primary_artist": mock_primary_artist_data,
        "album": None,  # Or mock album data if needed
        "api_path": "/songs/10101",
        "annotation_count": 3,
        "header_image_thumbnail_url": "https://example.com/assert-thumb.jpg",
        "header_image_url": "https://example.com/assert-header.jpg",
        "lyrics_owner_id": 12345,
        "lyrics_state": "complete",
        "pyongs_count": 10,
        "song_art_image_thumbnail_url": "https://example.com/assert-art-thumb.jpg",
        "song_art_image_url": "https://example.com/assert-art.jpg",
        "title_with_featured": "Assert Equals Blues",
        "url": "https://genius.com/Pytest-fixture-assert-equals-blues-lyrics",
        "stats": {"pageviews": 1234, "unreviewed_annotations": 1, "hot": False},
        "featured_artists": [],
    }
    song2 = {
        "id": 10102,
        "title": "Patch Decorator Funk",
        "full_title": "Patch Decorator Funk by Pytest Fixture",
        "path": "/Pytest-fixture-patch-decorator-funk-lyrics",
        "primary_artist": mock_primary_artist_data,
        "album": None,
        "api_path": "/songs/10102",
        "annotation_count": 5,
        "header_image_thumbnail_url": "https://example.com/patch-thumb.jpg",
        "header_image_url": "https://example.com/patch-header.jpg",
        "lyrics_owner_id": 12345,
        "lyrics_state": "complete",
        "pyongs_count": 15,
        "song_art_image_thumbnail_url": "https://example.com/patch-art-thumb.jpg",
        "song_art_image_url": "https://example.com/patch-art.jpg",
        "title_with_featured": "Patch Decorator Funk",
        "url": "https://genius.com/Pytest-fixture-patch-decorator-funk-lyrics",
        "stats": {"pageviews": 5678, "unreviewed_annotations": 0, "hot": True},
        "featured_artists": [],
    }
    return [song1, song2]


@pytest.fixture
def mock_primary_songs_lyrics() -> list[str]:
    """Mock lyrics for the primary artist's songs."""
    return [
        "[Verse 1]\nCheck the value, is it true?\nAssert equals, me and you.\n[Chorus]\nOh, the assert equals blues!",
        "[Intro]\nPatch it up, patch it in!\n[Verse 1]\nDecorate the function call,\nMock the world, stand up tall.",
    ]


@pytest.fixture
def mock_another_artist_data() -> dict[str, Any]:
    """Mock data for a different artist."""
    return {
        "id": 1002,
        "name": "Mock Runner",
        "url": "https://genius.com/artists/Mock-runner",
        "api_path": "/artists/1002",
        "header_image_url": "...",
        "image_url": "...",
        "is_meme_verified": False,
        "is_verified": False,
    }


@pytest.fixture
def mock_another_song_data(mock_another_artist_data: dict[str, Any]) -> dict[str, Any]:
    """Mock data for the different artist's song, matching test_song.py structure."""
    return {
        "id": 10201,
        "title": "Side Effect Ballad",
        "full_title": "Side Effect Ballad by Mock Runner",
        "path": "/Mock-runner-side-effect-ballad-lyrics",
        "primary_artist": mock_another_artist_data,
        "album": None,
        "api_path": "/songs/10201",
        "annotation_count": 2,
        "header_image_thumbnail_url": "https://example.com/sideeffect-thumb.jpg",
        "header_image_url": "https://example.com/sideeffect-header.jpg",
        "lyrics_owner_id": 67890,
        "lyrics_state": "complete",
        "pyongs_count": 5,
        "song_art_image_thumbnail_url": "https://example.com/sideeffect-art-thumb.jpg",
        "song_art_image_url": "https://example.com/sideeffect-art.jpg",
        "title_with_featured": "Side Effect Ballad",
        "url": "https://genius.com/Mock-runner-side-effect-ballad-lyrics",
        "stats": {"pageviews": 987, "unreviewed_annotations": 0, "hot": False},
        "featured_artists": [],
    }


@pytest.fixture
def mock_another_song_lyrics() -> str:
    """Mock lyrics for the different artist's song."""
    return "[Verse 1]\nDon't change the state, keep it clean,\nSide effects are rarely seen...\n[Outro]\nPure functions win."


@pytest.fixture
def mock_featured_artist_data() -> dict[str, Any]:
    """Mock data for a featured artist."""
    return {
        "id": 1003,
        "name": "Coverage Reporter",
        "url": "https://genius.com/artists/Coverage-reporter",
        "api_path": "/artists/1003",
        "header_image_url": "...",
        "image_url": "...",
        "is_meme_verified": False,
        "is_verified": True,
    }


@pytest.fixture
def mock_song_with_feature_data(
    mock_primary_artist_data: dict[str, Any], mock_featured_artist_data: dict[str, Any]
) -> dict[str, Any]:
    """Mock data for a song with a feature, matching test_song.py structure."""
    featured_artists_list = [mock_featured_artist_data]
    return {
        "id": 10301,
        "title": "Integration Test Jam",
        "full_title": f"Integration Test Jam by Pytest Fixture (Ft. {mock_featured_artist_data['name']})",
        "path": "/Pytest-fixture-integration-test-jam-lyrics",
        "primary_artist": mock_primary_artist_data,
        "album": None,
        "api_path": "/songs/10301",
        "annotation_count": 8,
        "header_image_thumbnail_url": "https://example.com/integration-thumb.jpg",
        "header_image_url": "https://example.com/integration-header.jpg",
        "lyrics_owner_id": 11223,
        "lyrics_state": "complete",
        "pyongs_count": 20,
        "song_art_image_thumbnail_url": "https://example.com/integration-art-thumb.jpg",
        "song_art_image_url": "https://example.com/integration-art.jpg",
        "title_with_featured": f"Integration Test Jam (Ft. {mock_featured_artist_data['name']})",
        "url": "https://genius.com/Pytest-fixture-integration-test-jam-lyrics",
        "stats": {"pageviews": 10101, "unreviewed_annotations": 2, "hot": True},
        "featured_artists": featured_artists_list,
    }


@pytest.fixture
def mock_song_with_feature_lyrics() -> str:
    """Mock lyrics for the song with a feature."""
    return "[Pytest Fixture - Verse 1]\nTesting units one by one...\n[Coverage Reporter - Verse 2]\nDid we hit that line? Check the run!"


@pytest.fixture
def song_to_add_data(mock_primary_artist_data: dict[str, Any]) -> dict[str, Any]:
    """Data for a new song to add, matching test_song.py structure."""
    return {
        "id": 10103,
        "title": "Refactor Rhapsody",
        "full_title": "Refactor Rhapsody by Pytest Fixture",
        "path": "/Pytest-fixture-refactor-rhapsody-lyrics",
        "primary_artist": mock_primary_artist_data,
        "album": None,
        "api_path": "/songs/10103",
        "annotation_count": 1,
        "header_image_thumbnail_url": "https://example.com/refactor-thumb.jpg",
        "header_image_url": "https://example.com/refactor-header.jpg",
        "lyrics_owner_id": 44556,
        "lyrics_state": "complete",
        "pyongs_count": 3,
        "song_art_image_thumbnail_url": "https://example.com/refactor-art-thumb.jpg",
        "song_art_image_url": "https://example.com/refactor-art.jpg",
        "title_with_featured": "Refactor Rhapsody",
        "url": "https://genius.com/Pytest-fixture-refactor-rhapsody-lyrics",
        "stats": {"pageviews": 555, "unreviewed_annotations": 0, "hot": False},
        "featured_artists": [],
    }


@pytest.fixture
def song_to_add_lyrics() -> str:
    """Lyrics for the new song to add."""
    return "[Verse 1]\nCode was messy, hard to read,\nTime to refactor, plant the seed."


@pytest.fixture
def song_to_add_object(
    song_to_add_lyrics: str, song_to_add_data: dict[str, Any]
) -> Song:
    """Creates the new Song object to add."""
    return Song(song_to_add_lyrics, song_to_add_data)


# --- Fixtures for Artist and Song Objects ---


@pytest.fixture
def primary_artist_songs(
    mock_primary_songs_lyrics: list[str], mock_primary_songs_data: list[dict[str, Any]]
) -> list[Song]:
    """Creates a list of mock Song objects for the primary artist."""
    songs = []
    for lyrics, data in zip(
        mock_primary_songs_lyrics, mock_primary_songs_data, strict=True
    ):
        songs.append(Song(lyrics, data))
    return songs


@pytest.fixture
def artist_object(
    mock_primary_artist_data: dict[str, Any], primary_artist_songs: list[Song]
) -> Artist:
    """Creates the primary Artist object populated with mock songs."""
    artist = Artist(mock_primary_artist_data)
    artist.songs = primary_artist_songs[:]
    return artist


@pytest.fixture
def another_artist_object(mock_another_artist_data: dict[str, Any]) -> Artist:
    """Creates the 'other' Artist object."""
    return Artist(mock_another_artist_data)


@pytest.fixture
def another_song_object(
    mock_another_song_lyrics: str, mock_another_song_data: dict[str, Any]
) -> Song:
    """Creates the 'other' Song object."""
    return Song(mock_another_song_lyrics, mock_another_song_data)


@pytest.fixture
def featured_artist_object(mock_featured_artist_data: dict[str, Any]) -> Artist:
    """Creates the featured Artist object."""
    return Artist(mock_featured_artist_data)


@pytest.fixture
def song_with_feature_object(
    mock_song_with_feature_lyrics: str, mock_song_with_feature_data: dict[str, Any]
) -> Song:
    """Creates the Song object that has a feature."""
    return Song(mock_song_with_feature_lyrics, mock_song_with_feature_data)


# --- Test Functions ---


def test_artist_instance(artist_object: Artist) -> None:
    """Test if the created object is an Artist instance."""
    assert isinstance(artist_object, Artist)


def test_name(artist_object: Artist, mock_primary_artist_data: dict[str, Any]) -> None:
    """Test if the artist object name matches the mock data."""
    assert artist_object.name == mock_primary_artist_data["name"]


def test_add_song_from_same_artist(
    artist_object: Artist, song_to_add_object: Song
) -> None:
    """Test adding a song by the same artist."""
    initial_song_count = artist_object.num_songs
    artist_object.add_song(song_to_add_object, verbose=False)
    assert artist_object.num_songs == initial_song_count + 1
    assert song_to_add_object in artist_object.songs
    # No need to manually clean up state, fixtures handle isolation


def test_song_retrieval(
    artist_object: Artist,
    primary_artist_songs: list[Song],
    mock_primary_songs_data: list[dict[str, Any]],
) -> None:
    """Test retrieving songs by title from the artist's list."""
    # Test finding the first song
    song_to_find_id = mock_primary_songs_data[0]["id"]
    song_to_find_title = primary_artist_songs[0].title
    found_song = artist_object.get_song(song_to_find_id)
    assert found_song is not None
    assert found_song.title == song_to_find_title
    assert found_song == primary_artist_songs[0]

    # Test finding the second song
    song_to_find_id_2 = mock_primary_songs_data[1]["id"]
    song_to_find_title_2 = primary_artist_songs[1].title
    found_song_2 = artist_object.get_song(song_to_find_id_2)
    assert found_song_2 is not None
    assert found_song_2.title == song_to_find_title_2
    assert found_song_2 == primary_artist_songs[1]

    # Test finding a non-existent song
    non_existent_song_id = 99999  # Use an unlikely integer ID
    found_song_none = artist_object.get_song(non_existent_song_id)
    assert found_song_none is None


def test_add_song_from_different_artist(
    artist_object: Artist, another_song_object: Song
) -> None:
    """Test attempting to add a song by a different artist."""
    initial_song_count = artist_object.num_songs
    artist_object.add_song(another_song_object, verbose=False)
    # Assert that the song count did NOT change
    assert artist_object.num_songs == initial_song_count
    assert another_song_object not in artist_object.songs


def test_add_song_with_includes_features(
    artist_object: Artist,
    featured_artist_object: Artist,
    song_with_feature_object: Song,
) -> None:
    """Test the include_features logic within add_song."""
    # song_with_feature_object has "Pytest Fixture" as primary, "Coverage Reporter" featured

    # 1. Add to primary artist (Pytest Fixture) - should work regardless of include_features
    initial_count_primary = artist_object.num_songs
    artist_object.add_song(
        song_with_feature_object, verbose=False, include_features=False
    )
    assert artist_object.num_songs == initial_count_primary + 1
    artist_object.songs.pop()  # Reset for next check

    artist_object.add_song(
        song_with_feature_object, verbose=False, include_features=True
    )
    assert artist_object.num_songs == initial_count_primary + 1
    artist_object.songs.pop()  # Clean up

    # 2. Add to featured artist (Coverage Reporter)
    initial_count_featured = featured_artist_object.num_songs
    assert initial_count_featured == 0  # Starts empty

    # Should succeed only if include_features=True
    featured_artist_object.add_song(
        song_with_feature_object, verbose=False, include_features=True
    )
    assert featured_artist_object.num_songs == initial_count_featured + 1
    assert song_with_feature_object in featured_artist_object.songs
    featured_artist_object.songs.pop()  # Reset

    # Should fail if include_features=False
    featured_artist_object.add_song(
        song_with_feature_object, verbose=False, include_features=False
    )
    assert featured_artist_object.num_songs == initial_count_featured
    assert song_with_feature_object not in featured_artist_object.songs


def test_saving_json_file(artist_object: Artist, tmp_path: Path) -> None:
    """Test saving the artist's data (mocked) to a JSON file using tmp_path."""
    extension = "json"
    # Use tmp_path fixture for temporary file
    filename_base = "Lyrics_" + artist_object.name.replace(" ", "")
    # Sanitize filename for the OS
    sanitized_base = sanitize_filename(filename_base)
    expected_filepath = tmp_path / f"{sanitized_base}.{extension}"

    # Test saving json file
    artist_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file()
    # Simple content check (can be more thorough)
    content = expected_filepath.read_text()
    assert f'"name": "{artist_object.name}' in content
    assert '"title": "Assert Equals Blues"' in content  # Check for a song title

    # Test overwriting json file
    # Modify lyrics of first song temporarily to check overwrite
    original_lyrics = artist_object.songs[0].lyrics
    artist_object.songs[0].lyrics = "Overwritten Lyrics Test"
    artist_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file()
    content_after_overwrite = expected_filepath.read_text()
    assert "Overwritten Lyrics Test" in content_after_overwrite
    # Restore original lyrics if needed for other tests (though fixtures usually isolate)
    artist_object.songs[0].lyrics = original_lyrics


def test_saving_txt_file(artist_object: Artist, tmp_path: Path) -> None:
    """Test saving the artist's data (mocked) to a TXT file using tmp_path."""
    extension = "txt"
    # Use tmp_path fixture for temporary file
    filename_base = "Lyrics_" + artist_object.name.replace(" ", "")
    # Sanitize filename for the OS
    sanitized_base = sanitize_filename(filename_base)
    expected_filepath = tmp_path / f"{sanitized_base}.{extension}"

    # Test saving txt file
    artist_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file()
    # Simple content check
    content = expected_filepath.read_text()
    assert "Assert Equals Blues" in content  # Check for song title
    assert "[Chorus]" in content  # Check for lyrics content

    # Test overwriting txt file
    # Modify lyrics of first song temporarily to check overwrite
    original_lyrics = artist_object.songs[0].lyrics
    artist_object.songs[0].lyrics = "Overwritten Lyrics Test for TXT"
    artist_object.save_lyrics(
        filename=str(expected_filepath),
        extension=extension,
        overwrite=True,
        sanitize=False,
        verbose=False,
    )
    assert expected_filepath.is_file()
    content_after_overwrite = expected_filepath.read_text()
    assert "Overwritten Lyrics Test for TXT" in content_after_overwrite
    # Restore original lyrics
    artist_object.songs[0].lyrics = original_lyrics
