"""Tests for how search_song picks a result, with the search endpoints mocked."""

from typing import Any
from unittest import mock

from lyricsgenius import Genius


def _song_hit(song_id: int, title: str, artist: str) -> dict[str, Any]:
    """Builds a song search hit."""
    return {
        "index": "song",
        "result": {
            "id": song_id,
            "title": title,
            "primary_artist": {"name": artist},
            "lyrics_state": "incomplete",
            "instrumental": False,
            "url": f"https://example.com/{song_id}",
        },
    }


def _search_all_response(song_hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Builds a search_all response with the hits as top hit and song section."""
    return {
        "sections": [
            {"type": "top_hits", "hits": song_hits[:1]},
            {"type": "song", "hits": song_hits},
        ]
    }


def test_search_song_prefers_exact_title_with_matching_artist() -> None:
    """Among results with the same title, the one by the requested artist wins."""
    g = Genius("dummy_access_token", sleep_time=0, skip_non_songs=False)
    search_all_response = _search_all_response(
        [
            _song_hit(1, "Santa", "Fedez"),
            _song_hit(2, "Santa", "Madonna"),
        ]
    )

    with (
        mock.patch.object(g, "search_all", return_value=search_all_response),
        mock.patch.object(g, "search", return_value={"hits": []}),
    ):
        result = g.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is not None
    assert result.title == "Santa"
    assert result.artist == "Madonna"


def test_search_song_returns_none_when_artist_does_not_match() -> None:
    """No song is returned when no result is by the requested artist."""
    g = Genius("dummy_access_token", sleep_time=0, skip_non_songs=False)
    search_all_response = _search_all_response([_song_hit(1, "Santa", "Fedez")])

    with (
        mock.patch.object(g, "search_all", return_value=search_all_response),
        mock.patch.object(g, "search", return_value={"hits": []}),
    ):
        result = g.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is None


def test_search_song_tolerates_hit_missing_title() -> None:
    """A hit without a title is skipped rather than raising."""
    g = Genius("dummy_access_token", sleep_time=0, skip_non_songs=False)
    malformed = _song_hit(1, "Santa", "Madonna")
    del malformed["result"]["title"]
    search_all_response = _search_all_response(
        [malformed, _song_hit(2, "Santa", "Madonna")]
    )

    with (
        mock.patch.object(g, "search_all", return_value=search_all_response),
        mock.patch.object(g, "search", return_value={"hits": []}),
    ):
        result = g.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is not None
    assert result.artist == "Madonna"


def test_search_song_tolerates_hit_missing_primary_artist() -> None:
    """A hit without a primary artist is skipped rather than raising."""
    g = Genius("dummy_access_token", sleep_time=0, skip_non_songs=True)
    malformed = _song_hit(1, "Santa", "Madonna")
    del malformed["result"]["primary_artist"]
    search_all_response = _search_all_response([malformed])

    with (
        mock.patch.object(g, "search_all", return_value=search_all_response),
        mock.patch.object(g, "search", return_value={"hits": []}),
    ):
        result = g.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is None


def test_search_song_returns_none_for_empty_title(genius: Genius) -> None:
    """An empty title finds nothing and makes no request."""
    with (
        mock.patch.object(genius, "search_all") as search_all,
        mock.patch.object(genius, "search") as search,
    ):
        result = genius.search_song("")

    assert result is None
    search_all.assert_not_called()
    search.assert_not_called()
