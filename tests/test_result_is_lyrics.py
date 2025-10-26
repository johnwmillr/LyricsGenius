from typing import Any

import pytest

from lyricsgenius.genius import Genius


@pytest.fixture()
def _result_is_lyrics_genius() -> Genius:
    """Provide a Genius instance for _result_is_lyrics tests with verbosity off."""
    return Genius(access_token="dummy_token_for_testing", verbose=False)


def _call(g: Genius, song: dict[str, Any]) -> bool:
    return g._result_is_lyrics(song)


@pytest.mark.parametrize(
    "song,expected",
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
            id="default_excluded_term",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "Hello World"},
            True,
            id="valid_song_title",
        ),
    ],
)
def test_result_is_lyrics_basic_cases(
    _result_is_lyrics_genius: Genius, song: dict[str, Any], expected: bool
) -> None:
    assert _call(_result_is_lyrics_genius, song) is expected


@pytest.mark.parametrize(
    "title,expected",
    [
        pytest.param("Bonus Track", False, id="excluded_via_custom_term"),
        pytest.param("Track List", False, id="default_term_still_excluded"),
        pytest.param("Tracklist", False, id="default_term_one_word_also_excluded"),
        pytest.param("Hello World", True, id="not_excluded"),
    ],
)
def test_custom_excluded_term_added_without_replacement(
    title: str, expected: bool
) -> None:
    g = Genius(
        access_token="dummy_token_for_testing",
        verbose=False,
        excluded_terms=["bonus track"],
        replace_default_terms=False,
    )
    assert _call(g, {"lyrics_state": "complete", "title": title}) is expected


@pytest.mark.parametrize(
    "title,expected",
    [
        pytest.param("Track List", True, id="default_term_no_longer_excluded"),
        pytest.param("Bonus Track", False, id="custom_term_still_excludes"),
        pytest.param("Song (Remix)", False, id="literal_parens_match_exactly"),
        pytest.param("Song Remix", True, id="without_parens_does_not_match"),
        pytest.param("Hello World", True, id="not_excluded"),
    ],
)
def test_replacing_default_terms_removes_original_exclusions(
    title: str, expected: bool
) -> None:
    g = Genius(
        access_token="dummy_token_for_testing",
        verbose=False,
        excluded_terms=["bonus track", "(Remix)"],
        replace_default_terms=True,
    )
    assert _call(g, {"lyrics_state": "complete", "title": title}) is expected
