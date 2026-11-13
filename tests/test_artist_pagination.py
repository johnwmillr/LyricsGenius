"""Tests for how search_artist pages through search results to find an artist."""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius


def _artist_hit(id_: int, name: str) -> dict[str, Any]:
    """Builds an artist search hit."""
    return {"index": "artist", "result": {"id": id_, "name": name}}


def _search_response(artist_hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Builds a search_all response whose artist section holds the given hits."""
    return {
        "sections": [
            # The first section is read as the top hits.
            {"type": "top_hits", "hits": artist_hits[:1]},
            {"type": "artist", "hits": artist_hits},
            {"type": "song", "hits": []},
        ]
    }


def _artist_info(id_: int, name: str) -> dict[str, Any]:
    """Builds the minimal artist response the Artist type accepts."""
    return {
        "artist": {
            "id": id_,
            "name": name,
            "url": f"https://genius.com/artists/{name.replace(' ', '-')}",
            "api_path": f"/artists/{id_}",
            "header_image_url": "https://example.com/header.jpg",
            "image_url": "https://example.com/image.jpg",
            "is_meme_verified": False,
            "is_verified": False,
        }
    }


@contextmanager
def _mocked_search(
    genius: Genius, pages: list[dict[str, Any]], artist: dict[str, Any] | None = None
) -> Iterator[tuple[mock.Mock, mock.Mock]]:
    """Serves the pages from search_all in order and the artist from artist()."""
    with (
        mock.patch.object(genius, "search_all", side_effect=pages) as search_all,
        mock.patch.object(genius, "artist", return_value=artist) as artist_lookup,
        mock.patch.object(
            genius, "artist_songs", return_value={"songs": [], "next_page": None}
        ),
    ):
        yield search_all, artist_lookup


@pytest.mark.parametrize("per_page", [0, -1, 6, 50, 100])
def test_genius_rejects_out_of_range_per_page(per_page: int) -> None:
    """per_page outside 1 to 5 is rejected, since search_all can't serve it."""
    with pytest.raises(ValueError, match="per_page must be between 1 and 5"):
        Genius("dummy_token", sleep_time=0, per_page=per_page)


@pytest.mark.parametrize("per_page", [1, 2, 3, 4, 5])
def test_genius_accepts_per_page_from_one_to_five(per_page: int) -> None:
    """per_page from 1 to 5 is kept as given."""
    client = Genius("dummy_token", sleep_time=0, per_page=per_page)

    assert client.per_page == per_page


def test_search_artist_finds_exact_match_on_a_later_page(genius: Genius) -> None:
    """Paging continues past a full page without an exact match."""
    pages = [
        _search_response(
            [_artist_hit(i, f"Radiohead Tribute {i}") for i in range(1, 6)]
        ),
        _search_response([_artist_hit(99, "Radiohead")]),
    ]

    with _mocked_search(genius, pages, _artist_info(99, "Radiohead")) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 2
    artist_lookup.assert_called_once_with(99)
    assert artist is not None
    assert artist.name == "Radiohead"


def test_search_artist_falls_back_to_first_page_result(genius: Genius) -> None:
    """Without an exact match, the best result from the first page is used."""
    pages = [
        _search_response(
            [
                _artist_hit(1, "Radiohead Tribute"),
                *[_artist_hit(i, f"Radiohead Fan {i}") for i in range(2, 6)],
            ]
        ),
        _search_response([_artist_hit(99, "Radiohead something else")]),
    ]

    with _mocked_search(genius, pages, _artist_info(1, "Radiohead Tribute")) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 2
    artist_lookup.assert_called_once_with(1)
    assert artist is not None
    assert artist.name == "Radiohead Tribute"


def test_search_artist_stops_when_no_artists_are_found(genius: Genius) -> None:
    """An empty artist section ends the search with no artist."""
    with _mocked_search(genius, [_search_response([])]) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 1
    artist_lookup.assert_not_called()
    assert artist is None


def test_search_artist_stops_after_a_partial_page(genius: Genius) -> None:
    """A page that isn't full is the last one, so no further page is requested."""
    pages = [_search_response([_artist_hit(1, "Radiohead Fan")])]

    with _mocked_search(genius, pages, _artist_info(1, "Radiohead Fan")) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 1
    artist_lookup.assert_called_once_with(1)
    assert artist is not None
    assert artist.name == "Radiohead Fan"


def test_search_artist_stops_after_ten_pages(genius: Genius) -> None:
    """Paging stops after ten full pages even if none has an exact match."""
    full_page = _search_response(
        [_artist_hit(i, f"Radiohead Clone {i}") for i in range(5)]
    )

    with _mocked_search(
        genius, [full_page] * 11, _artist_info(0, "Radiohead Clone 0")
    ) as mocks:
        genius.search_artist("Radiohead", max_songs=0)

    search_all, _ = mocks
    assert search_all.call_count == 10
