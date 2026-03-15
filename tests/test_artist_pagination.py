"""Unit tests for artist-search pagination logic in Genius.search_artist().

These tests verify the behavior of find_artist_id() without making real API
calls by mocking Genius.search_all() and Genius.artist().
"""

from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _artist_hit(id_: int, name: str) -> dict[str, Any]:
    return {"index": "artist", "result": {"id": id_, "name": name}}


def _search_response(artist_hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a minimal search_all(type_='multi') response dict."""
    return {
        "sections": [
            # sections[0] is used as "top hits" by _get_item_from_search_response
            {"type": "top_hits", "hits": artist_hits[:1]},
            {"type": "artist", "hits": artist_hits},
            {"type": "song", "hits": []},
        ]
    }


def _artist_info(id_: int, name: str) -> dict[str, Any]:
    """Minimal artist body accepted by the Artist type."""
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


@pytest.fixture
def g() -> Genius:
    """Genius instance with a dummy token; no real API calls are made."""
    return Genius("dummy_access_token", sleep_time=0, per_page=5)


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------


class TestPerPageValidation:
    """per_page must be in [1, 5] when using search_all(type_='multi')."""

    @pytest.mark.parametrize("bad_value", [0, -1, 6, 50, 100])
    def test_raises_for_out_of_range_values(self, bad_value: int) -> None:
        with pytest.raises(ValueError, match="per_page must be between 1 and 5"):
            Genius("dummy_token", sleep_time=0, per_page=bad_value)

    @pytest.mark.parametrize("good_value", [1, 2, 3, 4, 5])
    def test_accepts_valid_values(self, good_value: int) -> None:
        client = Genius("dummy_token", sleep_time=0, per_page=good_value)
        assert client.per_page == good_value


# ---------------------------------------------------------------------------
# Pagination behaviour tests
# ---------------------------------------------------------------------------


class TestArtistSearchPagination:
    def test_finds_exact_match_on_page_2(self, g: Genius) -> None:
        """search_artist() should continue paginating to find an exact match."""
        # Page 1: 5 non-exact hits (full page → has more pages)
        page1_hits = [_artist_hit(i, f"Radiohead Tribute {i}") for i in range(1, 6)]
        # Page 2: 1 exact hit (partial page → last page)
        page2_hits = [_artist_hit(99, "Radiohead")]

        responses = [_search_response(page1_hits), _search_response(page2_hits)]
        call_count = 0

        def mock_search_all(
            term: str, per_page: int = 5, page: int = 1
        ) -> dict[str, Any]:
            nonlocal call_count
            resp = responses[call_count]
            call_count += 1
            return resp

        with (
            mock.patch.object(g, "search_all", side_effect=mock_search_all),
            mock.patch.object(g, "artist", return_value=_artist_info(99, "Radiohead")),
            mock.patch.object(
                g, "artist_songs", return_value={"songs": [], "next_page": None}
            ),
        ):
            result = g.search_artist("Radiohead", max_songs=0)

        assert call_count == 2, "Should have called search_all twice (page 1 and 2)"
        assert result is not None
        assert result.name == "Radiohead"

    def test_fallback_uses_page_1_candidate_not_last_page(self, g: Genius) -> None:
        """When no exact match is found, the fallback should be the page-1 result."""
        # Page 1: 5 non-exact hits (full page → try page 2)
        page1_hits = [
            _artist_hit(1, "Radiohead Tribute"),
            *[_artist_hit(i, f"Radiohead Fan {i}") for i in range(2, 6)],
        ]
        # Page 2: 1 non-exact hit (partial → last page, no exact match)
        page2_hits = [_artist_hit(99, "Radiohead something else")]

        responses = [_search_response(page1_hits), _search_response(page2_hits)]
        call_count = 0

        def mock_search_all(
            term: str, per_page: int = 5, page: int = 1
        ) -> dict[str, Any]:
            nonlocal call_count
            resp = responses[call_count]
            call_count += 1
            return resp

        # search_artist will call self.artist(1) — the page-1 candidate's id
        with (
            mock.patch.object(g, "search_all", side_effect=mock_search_all),
            mock.patch.object(
                g, "artist", return_value=_artist_info(1, "Radiohead Tribute")
            ),
            mock.patch.object(
                g, "artist_songs", return_value={"songs": [], "next_page": None}
            ),
        ):
            result = g.search_artist("Radiohead", max_songs=0)

        assert call_count == 2
        assert result is not None
        # Should fall back to the page-1 candidate (id=1), NOT the page-2 result (id=99)
        assert result.name == "Radiohead Tribute"

    def test_stops_when_artist_section_is_empty(self, g: Genius) -> None:
        """Pagination should stop immediately when the artist section has no hits."""
        empty_response = _search_response([])  # no artist hits on page 1

        call_count = 0

        def mock_search_all(
            term: str, per_page: int = 5, page: int = 1
        ) -> dict[str, Any]:
            nonlocal call_count
            call_count += 1
            return empty_response

        with mock.patch.object(g, "search_all", side_effect=mock_search_all):
            result = g.search_artist("Radiohead", max_songs=0)

        assert call_count == 1, "Should stop after first empty page"
        assert result is None

    def test_stops_after_partial_page_with_no_exact_match(self, g: Genius) -> None:
        """Should not request a further page when the artist section is not full."""
        partial_hits = [_artist_hit(1, "Radiohead Fan")]  # only 1 hit (< per_page=5)

        call_count = 0

        def mock_search_all(
            term: str, per_page: int = 5, page: int = 1
        ) -> dict[str, Any]:
            nonlocal call_count
            call_count += 1
            return _search_response(partial_hits)

        with (
            mock.patch.object(g, "search_all", side_effect=mock_search_all),
            mock.patch.object(
                g, "artist", return_value=_artist_info(1, "Radiohead Fan")
            ),
            mock.patch.object(
                g, "artist_songs", return_value={"songs": [], "next_page": None}
            ),
        ):
            result = g.search_artist("Radiohead", max_songs=0)

        assert call_count == 1, "Should not paginate when page is not full"
        # Falls back to the only candidate
        assert result is not None
        assert result.name == "Radiohead Fan"

    def test_max_pages_cap_prevents_infinite_loop(self, g: Genius) -> None:
        """Pagination must stop after max_pages=10 (default) even with always-full pages."""
        full_non_matching_hits = [
            _artist_hit(i, f"Radiohead Clone {i}") for i in range(5)
        ]

        call_count = 0

        def mock_search_all(
            term: str, per_page: int = 5, page: int = 1
        ) -> dict[str, Any]:
            nonlocal call_count
            call_count += 1
            return _search_response(full_non_matching_hits)

        with (
            mock.patch.object(g, "search_all", side_effect=mock_search_all),
            mock.patch.object(
                g, "artist", return_value=_artist_info(0, "Radiohead Clone 0")
            ),
            mock.patch.object(
                g, "artist_songs", return_value={"songs": [], "next_page": None}
            ),
        ):
            g.search_artist("Radiohead", max_songs=0)

        assert call_count == 10, "Should stop after max_pages=10 pages (default)"
