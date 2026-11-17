"""Tests for how Genius decides whether a search result is a song with lyrics."""

from typing import Any

import pytest

from lyricsgenius.genius import Genius


@pytest.mark.parametrize(
    ("song", "expected"),
    [
        pytest.param(
            {"lyrics_state": "incomplete", "title": "Some Song"},
            False,
            id="incomplete_lyrics_state",
        ),
        pytest.param(
            {"lyrics_state": "complete", "instrumental": True, "title": "Piano Solo"},
            False,
            id="instrumental_flag",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "Track List"},
            False,
            id="default_excluded_term",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "[Track List]"},
            False,
            id="bracketed_default_excluded_term",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "Hello World"},
            True,
            id="valid_song_title",
        ),
    ],
)
def test_result_is_lyrics_classifies_results(
    genius: Genius, song: dict[str, Any], expected: bool
) -> None:
    """Only complete, non-instrumental results with allowed titles have lyrics."""
    assert genius._result_is_lyrics(song) is expected


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        pytest.param("Bonus Track", False, id="excluded_via_custom_term"),
        pytest.param("Track List", False, id="default_term_still_excluded"),
        pytest.param("Tracklist", False, id="default_term_one_word_also_excluded"),
        pytest.param("Hello World", True, id="not_excluded"),
    ],
)
def test_result_is_lyrics_adds_custom_terms_to_defaults(
    title: str, expected: bool
) -> None:
    """Custom excluded terms apply alongside the default ones."""
    g = Genius(
        access_token="dummy_token_for_testing",
        excluded_terms=["bonus track"],
        replace_default_terms=False,
    )

    assert g._result_is_lyrics({"lyrics_state": "complete", "title": title}) is expected


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        pytest.param("Track List", True, id="default_term_no_longer_excluded"),
        pytest.param("Bonus Track", False, id="custom_term_still_excludes"),
        pytest.param("Song (Remix)", False, id="literal_parens_match_exactly"),
        pytest.param("Song Remix", True, id="without_parens_does_not_match"),
        pytest.param("Hello World", True, id="not_excluded"),
    ],
)
def test_result_is_lyrics_can_replace_default_terms(title: str, expected: bool) -> None:
    """Replacing the default terms leaves only the custom ones, matched literally."""
    g = Genius(
        access_token="dummy_token_for_testing",
        excluded_terms=["bonus track", "(Remix)"],
        replace_default_terms=True,
    )

    assert g._result_is_lyrics({"lyrics_state": "complete", "title": title}) is expected
