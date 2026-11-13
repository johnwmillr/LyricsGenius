"""Tests for search_song: picking a result and building the Song, with requests mocked."""

from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius


def _song_hit(
    song_id: int, title: str, artist: str, lyrics_state: str = "incomplete"
) -> dict[str, Any]:
    """Builds a song search hit."""
    return {
        "index": "song",
        "result": {
            "id": song_id,
            "title": title,
            "primary_artist": {"name": artist},
            "lyrics_state": lyrics_state,
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
    assert result._body["id"] == 2


def test_search_song_tolerates_hit_missing_primary_artist() -> None:
    """A hit without a primary artist is skipped rather than raising."""
    g = Genius("dummy_access_token", sleep_time=0, skip_non_songs=False)
    malformed = _song_hit(1, "Santa", "Madonna")
    del malformed["result"]["primary_artist"]
    search_all_response = _search_all_response(
        [malformed, _song_hit(2, "Santa", "Madonna")]
    )

    with (
        mock.patch.object(g, "search_all", return_value=search_all_response),
        mock.patch.object(g, "search", return_value={"hits": []}),
    ):
        result = g.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is not None
    assert result._body["id"] == 2


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


_NO_SONG_RESULTS = {"sections": [{"type": "top_hits", "hits": []}]}


def test_search_song_searches_title_with_artist(genius: Genius) -> None:
    """The search term combines the title and artist."""
    with (
        mock.patch.object(
            genius, "search_all", return_value=_NO_SONG_RESULTS
        ) as search_all,
        mock.patch.object(genius, "search", return_value={"hits": []}),
    ):
        genius.search_song("Santa", artist="Madonna")

    search_all.assert_called_once_with("Santa Madonna")


def test_search_song_falls_back_to_plain_search(genius: Genius) -> None:
    """When search_all has no match, the plain search's exact match is used."""
    genius.skip_non_songs = False
    hits = [_song_hit(4, "Santa", "Fedez"), _song_hit(5, "Santa", "Madonna")]

    with (
        mock.patch.object(genius, "search_all", return_value=_NO_SONG_RESULTS),
        mock.patch.object(genius, "search", return_value={"hits": hits}) as search,
    ):
        result = genius.search_song("Santa", artist="Madonna", get_full_info=False)

    search.assert_called_once_with("Santa Madonna")
    assert result is not None
    assert result._body["id"] == 5


def test_search_song_fallback_keeps_artist_filter(genius: Genius) -> None:
    """Without an exact title match, the fallback takes the requested artist's hit."""
    genius.skip_non_songs = False
    hits = [_song_hit(4, "Santa Live", "Fedez"), _song_hit(5, "Santa Live", "Madonna")]

    with (
        mock.patch.object(genius, "search_all", return_value=_NO_SONG_RESULTS),
        mock.patch.object(genius, "search", return_value={"hits": hits}),
    ):
        result = genius.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is not None
    assert result._body["id"] == 5


def test_search_song_returns_lyrics_of_complete_song(genius: Genius) -> None:
    """A song with complete lyrics comes back with the lyrics from its page."""
    hit = _song_hit(1, "Santa", "Madonna", lyrics_state="complete")

    with (
        mock.patch.object(
            genius, "search_all", return_value=_search_all_response([hit])
        ),
        mock.patch.object(genius, "lyrics", return_value="words") as lyrics,
    ):
        result = genius.search_song("Santa", artist="Madonna", get_full_info=False)

    lyrics.assert_called_once_with(song_url="https://example.com/1")
    assert result is not None
    assert result.lyrics == "words"


@pytest.mark.parametrize(
    ("lyrics_state", "page_lyrics"),
    [
        pytest.param("incomplete", "words", id="incomplete_lyrics"),
        pytest.param("complete", None, id="lyrics_not_found"),
    ],
)
def test_search_song_rejects_songs_without_lyrics(
    genius: Genius, lyrics_state: str, page_lyrics: str | None
) -> None:
    """With skip_non_songs, a song with no lyrics to return is rejected."""
    hit = _song_hit(1, "Santa", "Madonna", lyrics_state=lyrics_state)

    with (
        mock.patch.object(
            genius, "search_all", return_value=_search_all_response([hit])
        ),
        mock.patch.object(genius, "search", return_value={"hits": []}),
        mock.patch.object(genius, "lyrics", return_value=page_lyrics),
    ):
        result = genius.search_song("Santa", artist="Madonna", get_full_info=False)

    assert result is None


def test_search_song_merges_full_song_info(genius: Genius) -> None:
    """With get_full_info, the song's full data is fetched by ID and merged in."""
    genius.skip_non_songs = False
    hit = _song_hit(1, "Santa", "Madonna")

    with (
        mock.patch.object(
            genius, "search_all", return_value=_search_all_response([hit])
        ),
        mock.patch.object(
            genius, "song", return_value={"song": {"release_date": "2026-01-01"}}
        ) as song,
    ):
        result = genius.search_song("Santa", artist="Madonna")

    song.assert_called_once_with(1)
    assert result is not None
    assert result._body["release_date"] == "2026-01-01"


def test_search_song_by_id_skips_search(genius: Genius) -> None:
    """A song ID is looked up directly, without searching."""
    genius.skip_non_songs = False
    body = _song_hit(9, "Santa", "Madonna")["result"]

    with (
        mock.patch.object(genius, "song", return_value={"song": body}) as song,
        mock.patch.object(genius, "search_all") as search_all,
    ):
        result = genius.search_song(song_id=9)

    song.assert_called_once_with(9)
    search_all.assert_not_called()
    assert result is not None
    assert result.title == "Santa"
