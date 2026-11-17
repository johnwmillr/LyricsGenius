"""Tests for the Album type and search_album, using invented album data."""

import json
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius
from lyricsgenius.types import Album, Song

TRACK_LYRICS = [
    "[Verse 1]\nArrange the mocks, prepare the scene,\nBefore the test, keep it clean.",
    "[Verse 1]\nReset the state, undo the change,\nAfter the test, rearrange.",
]


@pytest.fixture
def album_data() -> dict[str, Any]:
    """Provides the data for the invented album "Mocking the Tests"."""
    return json.loads(Path("tests/fixtures/album_info_mocked.json").read_text())


@pytest.fixture
def track_data() -> list[dict[str, Any]]:
    """Provides the data for the album's two invented tracks."""
    songs = json.loads(Path("tests/fixtures/song_info_mocked.json").read_text())
    return songs[:2]


@pytest.fixture
def album(album_data: dict[str, Any], track_data: list[dict[str, Any]]) -> Album:
    """Provides an Album holding the two tracks with their lyrics."""
    tracks = [
        Song(lyrics, data)
        for lyrics, data in zip(TRACK_LYRICS, track_data, strict=True)
    ]
    return Album(album_data, tracks)


def test_album_numbers_tracks_in_order(album: Album) -> None:
    """Tracks are numbered from 1 in the order they were given."""
    assert [(number, song.title) for number, song in album.tracks] == [
        (1, "Setup Serenade"),
        (2, "Teardown Tango"),
    ]


def test_album_parses_release_date(album: Album) -> None:
    """The release date components become a datetime."""
    assert album.release_date_components == datetime(2025, 4, 1)


def test_album_to_dict_includes_tracks_and_release_date(album: Album) -> None:
    """The dict form names the artist and holds each numbered track with lyrics."""
    album_dict = album.to_dict()

    assert album_dict["name"] == "Mocking the Tests"
    assert album_dict["artist"] == "Py Testerson"
    assert album_dict["release_date"] == "2025-04-01"
    assert [
        (track["number"], track["song"]["title"], track["song"]["lyrics"])
        for track in album_dict["tracks"]
    ] == [
        (1, "Setup Serenade", TRACK_LYRICS[0]),
        (2, "Teardown Tango", TRACK_LYRICS[1]),
    ]


def test_album_to_text_labels_each_track(album: Album) -> None:
    """The text form gives each track's number, title and lyrics."""
    assert album.to_text() == (
        f"[Track 1: Setup Serenade]\n{TRACK_LYRICS[0]}\n\n"
        f"[Track 2: Teardown Tango]\n{TRACK_LYRICS[1]}"
    )


@pytest.mark.parametrize("extension", ["json", "txt"])
def test_album_save_lyrics_writes_serialized_album(
    album: Album, tmp_path: Path, extension: str
) -> None:
    """Saving writes the album's JSON or text form to the file."""
    path = tmp_path / f"album.{extension}"

    album.save_lyrics(filename=str(tmp_path / "album"), extension=extension)

    if extension == "json":
        assert json.loads(path.read_text()) == album.to_dict()
    else:
        assert path.read_text() == album.to_text()


def test_album_save_lyrics_default_filename_uses_artist_and_name(
    album: Album, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without a filename, the file is named after the artist and album."""
    monkeypatch.chdir(tmp_path)

    album.save_lyrics(overwrite=True)

    assert [path.name for path in tmp_path.iterdir()] == [
        "saved_album_lyrics_py_testerson_mocking_the_tests.json"
    ]


def _search_hit(album_data: dict[str, Any]) -> dict[str, Any]:
    """Builds a search_all response whose only album hit is a minimal album."""
    minimal = {key: album_data[key] for key in ("id", "name", "artist")}
    hit = {"index": "album", "result": minimal}
    return {
        "sections": [
            {"type": "top_hits", "hits": [hit]},
            {"type": "album", "hits": [hit]},
        ]
    }


def _tracks_page(songs: list[dict[str, Any]], next_page: int | None) -> dict[str, Any]:
    """Builds one page of album_tracks results."""
    return {"tracks": [{"song": song} for song in songs], "next_page": next_page}


@contextmanager
def _mocked_album(
    genius: Genius, album_data: dict[str, Any], pages: list[dict[str, Any]]
) -> Iterator[tuple[mock.Mock, mock.Mock, mock.Mock, mock.Mock]]:
    """Serves the search, the full album, the track pages and lyrics per URL."""
    with (
        mock.patch.object(
            genius, "search_all", return_value=_search_hit(album_data)
        ) as search_all,
        mock.patch.object(
            genius, "album", return_value={"album": album_data}
        ) as album_lookup,
        mock.patch.object(genius, "album_tracks", side_effect=pages) as album_tracks,
        mock.patch.object(
            genius, "lyrics", side_effect=lambda song_url: f"lyrics of {song_url}"
        ) as lyrics,
    ):
        yield search_all, album_lookup, album_tracks, lyrics


def test_search_album_fetches_lyrics_for_each_track(
    genius: Genius, album_data: dict[str, Any], track_data: list[dict[str, Any]]
) -> None:
    """Each track with complete lyrics gets the lyrics from its page."""
    with _mocked_album(genius, album_data, [_tracks_page(track_data, None)]):
        album = genius.search_album("Mocking the Tests")

    assert album is not None
    assert [song.lyrics for _, song in album.tracks] == [
        f"lyrics of {song['url']}" for song in track_data
    ]


def test_search_album_can_skip_lyrics(
    genius: Genius, album_data: dict[str, Any], track_data: list[dict[str, Any]]
) -> None:
    """With fetch_lyrics=False, no lyrics are requested and tracks have none."""
    with _mocked_album(genius, album_data, [_tracks_page(track_data, None)]) as mocks:
        album = genius.search_album("Mocking the Tests", fetch_lyrics=False)

    *_, lyrics = mocks
    lyrics.assert_not_called()
    assert album is not None
    assert [song.lyrics for _, song in album.tracks] == ["", ""]


def test_search_album_pages_through_tracks(
    genius: Genius, album_data: dict[str, Any], track_data: list[dict[str, Any]]
) -> None:
    """Tracks are collected from every page of album_tracks."""
    pages = [_tracks_page(track_data[:1], 2), _tracks_page(track_data[1:], None)]

    with _mocked_album(genius, album_data, pages) as mocks:
        album = genius.search_album("Mocking the Tests", text_format="plain")

    _, _, album_tracks, _ = mocks
    assert album_tracks.call_args_list == [
        mock.call(album_id=album_data["id"], per_page=50, page=1, text_format="plain"),
        mock.call(album_id=album_data["id"], per_page=50, page=2, text_format="plain"),
    ]
    assert album is not None
    assert [song.title for _, song in album.tracks] == [
        "Setup Serenade",
        "Teardown Tango",
    ]


def test_search_album_merges_full_album_info(
    genius: Genius, album_data: dict[str, Any], track_data: list[dict[str, Any]]
) -> None:
    """The full album data is fetched for the search hit's ID and merged in."""
    with _mocked_album(genius, album_data, [_tracks_page(track_data, None)]) as mocks:
        album = genius.search_album("Mocking the Tests")

    _, album_lookup, _, _ = mocks
    album_lookup.assert_called_once_with(album_data["id"], None)
    assert album is not None
    assert album.url == album_data["url"]


def test_search_album_skips_lyrics_for_instrumentals(
    genius: Genius, album_data: dict[str, Any], track_data: list[dict[str, Any]]
) -> None:
    """Instrumental tracks are kept without requesting their lyrics."""
    instrumental = {**track_data[0], "instrumental": True}

    with _mocked_album(
        genius, album_data, [_tracks_page([instrumental], None)]
    ) as mocks:
        album = genius.search_album("Mocking the Tests")

    *_, lyrics = mocks
    lyrics.assert_not_called()
    assert album is not None
    assert [song.lyrics for _, song in album.tracks] == [""]


def test_search_album_by_id_skips_search(
    genius: Genius, album_data: dict[str, Any], track_data: list[dict[str, Any]]
) -> None:
    """An album ID is looked up directly, without searching."""
    with _mocked_album(genius, album_data, [_tracks_page(track_data, None)]) as mocks:
        album = genius.search_album(album_id=album_data["id"])

    search_all, album_lookup, _, _ = mocks
    search_all.assert_not_called()
    album_lookup.assert_called_once_with(album_data["id"], None)
    assert album is not None
    assert album.name == "Mocking the Tests"
