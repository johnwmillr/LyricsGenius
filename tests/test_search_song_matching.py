from typing import Any
from unittest import mock

from lyricsgenius import Genius


def _song_hit(song_id: int, title: str, artist: str) -> dict[str, Any]:
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
    return {
        "sections": [
            {"type": "top_hits", "hits": song_hits[:1]},
            {"type": "song", "hits": song_hits},
        ]
    }


def test_search_song_prefers_exact_title_with_matching_artist() -> None:
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
    g = Genius("dummy_access_token", sleep_time=0, skip_non_songs=False)
    search_all_response = _search_all_response([_song_hit(1, "Santa", "Fedez")])

    with (
        mock.patch.object(g, "search_all", return_value=search_all_response),
        mock.patch.object(g, "search", return_value={"hits": []}),
    ):
        result = g.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is None
