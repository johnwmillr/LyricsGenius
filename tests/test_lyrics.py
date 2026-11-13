"""Tests for scraping lyrics from a song page, using an invented page fixture."""

import logging
from pathlib import Path
from unittest import mock

import pytest

from lyricsgenius.genius import Genius, _preloaded_lyrics_html

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

EXPECTED_LYRICS_WITHOUT_HEADERS = (
    "Assert the true, mock the new\n"
    "Patch the world, see it through\n"
    "Arrange the state, don’t delay\n"
    "\n"
    "Call the function, watch it run\n"
    "Did it break?\n"
    "Was it “fun”?\n"
    "Capture output, every byte\n"
    "\n"
    "Check the value, is it right?\n"
    "Compare the strings, day and night\n"
    "Test complete, green light bright"
)


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


def _scrape(genius: Genius, page: str, **kwargs: bool) -> str | None:
    """Runs Genius.lyrics() against the given page HTML."""
    with mock.patch.object(genius, "_make_request", return_value={"html": page}):
        return genius.lyrics(song_url=SONG_URL, **kwargs)


def test_lyrics_reads_lyrics_containers(genius: Genius, song_page: str) -> None:
    """Lyrics are read from the page's lyrics containers, keeping line breaks."""
    assert _scrape(genius, song_page) == EXPECTED_LYRICS


def test_lyrics_falls_back_to_page_state(
    genius: Genius, song_page_without_containers: str
) -> None:
    """Without lyrics containers, lyrics are read from the page's embedded state."""
    assert _scrape(genius, song_page_without_containers) == EXPECTED_LYRICS


def test_lyrics_fallback_removes_section_headers(
    genius: Genius, song_page: str, song_page_without_containers: str
) -> None:
    """Both ways of reading lyrics remove headers and keep one blank line per gap."""
    from_containers = _scrape(genius, song_page, remove_section_headers=True)
    from_state = _scrape(
        genius, song_page_without_containers, remove_section_headers=True
    )

    assert from_containers == EXPECTED_LYRICS_WITHOUT_HEADERS
    assert from_state == EXPECTED_LYRICS_WITHOUT_HEADERS


def test_lyrics_containers_take_precedence(genius: Genius, song_page: str) -> None:
    """When both are present, the lyrics containers win over the embedded state."""
    page = song_page.replace("Call the function", "Call the containers", 1)

    lyrics = _scrape(genius, page)

    assert lyrics is not None
    assert "Call the containers" in lyrics


@pytest.mark.parametrize(
    "state",
    [
        pytest.param(None, id="no_state"),
        pytest.param(
            r"""window.__PRELOADED_STATE__ = JSON.parse('{\"songPage\":{}}');""",
            id="no_lyrics_data",
        ),
        pytest.param(
            r"""window.__PRELOADED_STATE__ = JSON.parse('not json');""",
            id="malformed_state",
        ),
        pytest.param(
            r"""window.__PRELOADED_STATE__ = JSON.parse('{\"songPage\":{\"lyricsData\":"""
            r"""{\"body\":{\"html\":\"<p></p>\"}}}}');""",
            id="empty_lyrics",
        ),
    ],
)
def test_lyrics_returns_none_when_nothing_is_found(
    genius: Genius, state: str | None, caplog: pytest.LogCaptureFixture
) -> None:
    """A page with no usable lyrics returns None and logs a warning."""
    page = f"<html><body><script>{state or ''}</script></body></html>"

    with caplog.at_level(logging.WARNING, logger="lyricsgenius.genius"):
        assert _scrape(genius, page) is None
    assert "Couldn't find the lyrics section" in caplog.text


def test_preloaded_lyrics_html_decodes_escaped_json() -> None:
    """JSON escapes inside the embedded JavaScript string are decoded once."""
    # A JSON string escape (\") inside the JS literal arrives as \\\"
    page = (
        r"""<script>window.__PRELOADED_STATE__ = JSON.parse('{\"songPage\":"""
        r"""{\"lyricsData\":{\"body\":{\"html\":"""
        r"""\"<a href=\\\"\/x\\\">It\'s</a>\"}}}}');</script>"""
    )
    assert _preloaded_lyrics_html(page) == '<a href="/x">It\'s</a>'


def test_lyrics_honors_client_remove_section_headers(song_page: str) -> None:
    """remove_section_headers set on the client applies to every lyrics call."""
    genius = Genius("dummy_access_token", sleep_time=0, remove_section_headers=True)

    assert _scrape(genius, song_page) == EXPECTED_LYRICS_WITHOUT_HEADERS


def test_lyrics_requests_page_path_from_url(genius: Genius, song_page: str) -> None:
    """The song URL is turned into a genius.com page path for the request."""
    with mock.patch.object(
        genius, "_make_request", return_value={"html": song_page}
    ) as request:
        genius.lyrics(song_url=SONG_URL)

    request.assert_called_once_with("Mocking-the-tests-lyrics", web=True)


def test_lyrics_finds_page_path_from_song_id(genius: Genius, song_page: str) -> None:
    """With a song ID, the page path comes from the song's API data."""
    with (
        mock.patch.object(
            genius, "song", return_value={"song": {"path": "/Mocking-the-tests-lyrics"}}
        ) as song,
        mock.patch.object(
            genius, "_make_request", return_value={"html": song_page}
        ) as request,
    ):
        lyrics = genius.lyrics(song_id=42)

    song.assert_called_once_with(42)
    request.assert_called_once_with("Mocking-the-tests-lyrics", web=True)
    assert lyrics == EXPECTED_LYRICS


def test_lyrics_requires_url_or_id(genius: Genius) -> None:
    """Lyrics need a song URL or a song ID."""
    with pytest.raises(ValueError, match="song_id"):
        genius.lyrics()


def test_lyrics_skips_elements_excluded_from_selection(
    genius: Genius, song_page: str
) -> None:
    """Elements Genius marks as excluded from selection aren't part of the lyrics."""
    page = song_page.replace(
        "Capture output, every byte",
        'Capture output, <div data-exclude-from-selection="true">Share</div>every byte',
        1,
    )

    assert _scrape(genius, page) == EXPECTED_LYRICS


def test_lyrics_removes_lyrics_header(genius: Genius, song_page: str) -> None:
    """The LyricsHeader block is removed even when not marked as excluded."""
    page = song_page.replace(
        'data-exclude-from-selection="true" class="LyricsHeader', 'class="LyricsHeader'
    )

    assert _scrape(genius, page) == EXPECTED_LYRICS


def test_lyrics_reads_empty_container_as_blank_line(
    genius: Genius, song_page: str
) -> None:
    """An empty lyrics container stands for a blank line between its neighbors."""
    second = '<div data-lyrics-container="true" class="Lyrics__Container-sc-12f9e8d3-1"><br><a'
    page = song_page.replace(
        second, '<div data-lyrics-container="true"></div>' + second, 1
    )

    assert page != song_page

    lyrics = _scrape(genius, page)

    assert lyrics == EXPECTED_LYRICS.replace("watch it run\n", "watch it run\n\n", 1)
