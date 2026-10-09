import logging
from pathlib import Path
from unittest import mock

import pytest

from lyricsgenius.genius import Genius, _decode_js_string, _preloaded_lyrics_html

SONG_URL = "https://genius.com/Mocking-the-tests-lyrics"

EXPECTED_LYRICS = (
    "[Setup]\n"
    "Assert the true, mock the new\n"
    "Patch the world, see it through\n"
    "Arrange the state, don’t delay\n"
    "\n"
    "[Act]\n"
    "Call the function, watch it run\n"
    "Did it break?\n"
    "Was it “fun”?\n"
    "Capture output, every byte\n"
    "\n"
    "[Assert]\n"
    "Check the value, is it right?\n"
    "Compare the strings, day and night\n"
    "Test complete, green light bright"
)


@pytest.fixture
def genius() -> Genius:
    return Genius("dummy_access_token", sleep_time=0)


@pytest.fixture
def song_page() -> str:
    """A song page with both lyrics containers and the embedded page state."""
    return Path("tests/fixtures/song_page.html").read_text(encoding="utf-8")


@pytest.fixture
def song_page_without_containers(song_page: str) -> str:
    """The same page as if Genius had changed its lyrics markup."""
    page = song_page.replace('data-lyrics-container="true"', 'data-gone="true"')
    assert 'data-lyrics-container="true"' not in page
    return page


def scrape(genius: Genius, page: str, **kwargs: bool) -> str | None:
    with mock.patch.object(genius, "_make_request", return_value={"html": page}):
        return genius.lyrics(song_url=SONG_URL, **kwargs)


def test_lyrics_from_containers(genius: Genius, song_page: str) -> None:
    assert scrape(genius, song_page) == EXPECTED_LYRICS


def test_lyrics_falls_back_to_page_state(
    genius: Genius, song_page_without_containers: str
) -> None:
    assert scrape(genius, song_page_without_containers) == EXPECTED_LYRICS


def test_fallback_removes_section_headers(
    genius: Genius, song_page: str, song_page_without_containers: str
) -> None:
    from_containers = scrape(genius, song_page, remove_section_headers=True)
    from_state = scrape(
        genius, song_page_without_containers, remove_section_headers=True
    )
    assert from_state == from_containers
    assert from_state is not None and "[Setup]" not in from_state


def test_lyrics_containers_take_precedence(genius: Genius, song_page: str) -> None:
    page = song_page.replace("Call the function", "Call the containers", 1)
    lyrics = scrape(genius, page)
    assert lyrics is not None and "Call the containers" in lyrics


@pytest.mark.parametrize(
    "state",
    [
        None,  # No embedded state at all
        r"""window.__PRELOADED_STATE__ = JSON.parse('{\"songPage\":{}}');""",
        r"""window.__PRELOADED_STATE__ = JSON.parse('not json');""",
        r"""window.__PRELOADED_STATE__ = JSON.parse('{\"songPage\":{\"lyricsData\":"""
        r"""{\"body\":{\"html\":\"<p></p>\"}}}}');""",
    ],
)
def test_lyrics_returns_none_when_nothing_is_found(
    genius: Genius, state: str | None, caplog: pytest.LogCaptureFixture
) -> None:
    page = f"<html><body><script>{state or ''}</script></body></html>"
    with caplog.at_level(logging.WARNING, logger="lyricsgenius.genius"):
        assert scrape(genius, page) is None
    assert "Couldn't find the lyrics section" in caplog.text


@pytest.mark.parametrize(
    ("literal", "expected"),
    [
        (r"plain", "plain"),
        (r"it\'s \"quoted\" \/ \\", 'it\'s "quoted" / \\'),
        (r"\x41B\u{43}", "ABC"),
        (r"line\nbreak\ttab", "line\nbreak\ttab"),
        (r"🎵", "🎵"),
        ("continued\\\nline", "continuedline"),
        (r"\q", "q"),
    ],
)
def test_decode_js_string(literal: str, expected: str) -> None:
    assert _decode_js_string(literal) == expected


def test_preloaded_lyrics_html_handles_escaped_json() -> None:
    # A JSON string escape (\") inside the JS literal arrives as \\\"
    page = (
        r"""<script>window.__PRELOADED_STATE__ = JSON.parse('{\"songPage\":"""
        r"""{\"lyricsData\":{\"body\":{\"html\":"""
        r"""\"<a href=\\\"\/x\\\">It\'s</a>\"}}}}');</script>"""
    )
    assert _preloaded_lyrics_html(page) == '<a href="/x">It\'s</a>'
