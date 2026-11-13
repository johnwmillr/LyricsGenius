"""Tests for the string, filename and URL helpers in lyricsgenius.utils."""

import pytest

from lyricsgenius.utils import (
    auth_from_environment,
    clean_str,
    decode_js_string,
    parse_redirected_url,
    sanitize_filename,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("B<ad File|_name", "Bad File_name", id="invalid_characters"),
        pytest.param('a:b"c?d*e>f', "abcdef", id="all_invalid_characters"),
        pytest.param("tab\there\x00", "tabhere", id="control_characters"),
        pytest.param("AC/DC - T.N.T.", "AC/DC - T.N.T.", id="slashes_and_dots_kept"),
        pytest.param("Sigur Rós", "Sigur Rós", id="accents_kept"),
    ],
)
def test_sanitize_filename_drops_only_invalid_characters(
    raw: str, expected: str
) -> None:
    """Filesystem-invalid and control characters are removed; the rest is kept."""
    assert sanitize_filename(raw) == expected


@pytest.mark.parametrize(
    ("literal", "expected"),
    [
        pytest.param(r"plain", "plain", id="plain"),
        pytest.param(r"it\'s \"quoted\" \/ \\", 'it\'s "quoted" / \\', id="quotes"),
        pytest.param(r"\x41B\u{43}", "ABC", id="hex_and_unicode_escapes"),
        pytest.param(r"line\nbreak\ttab", "line\nbreak\ttab", id="whitespace_escapes"),
        pytest.param(r"🎵", "\U0001f3b5", id="surrogate_pair"),
        pytest.param("continued\\\nline", "continuedline", id="line_continuation"),
        pytest.param(r"\q", "q", id="unknown_escape"),
    ],
)
def test_decode_js_string_decodes_escapes(literal: str, expected: str) -> None:
    """JavaScript string escapes decode to the characters they stand for."""
    assert decode_js_string(literal) == expected


@pytest.mark.parametrize(
    ("url", "flow"),
    [
        pytest.param("https://example.com/callback?code=test", "code", id="code"),
        pytest.param(
            "https://example.com/callback#access_token=test", "token", id="token"
        ),
    ],
)
def test_parse_redirected_url_extracts_flow_value(url: str, flow: str) -> None:
    """The code or token is read from the URL the user was redirected to."""
    assert parse_redirected_url(url, flow) == "test"


def test_parse_redirected_url_rejects_url_without_value() -> None:
    """A redirect URL without the expected parameter raises KeyError."""
    with pytest.raises(KeyError, match="code"):
        parse_redirected_url("https://example.com/callback?state=x", "code")


def test_auth_from_environment_reads_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Client ID, redirect URI and secret are read from their variables, in order."""
    monkeypatch.setenv("GENIUS_CLIENT_ID", "id")
    monkeypatch.setenv("GENIUS_REDIRECT_URI", "uri")
    monkeypatch.setenv("GENIUS_CLIENT_SECRET", "secret")

    assert auth_from_environment() == ("id", "uri", "secret")


def test_auth_from_environment_uses_none_for_missing_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Unset credential variables come back as None."""
    for name in ("GENIUS_CLIENT_ID", "GENIUS_REDIRECT_URI", "GENIUS_CLIENT_SECRET"):
        monkeypatch.delenv(name, raising=False)

    assert auth_from_environment() == (None, None, None)


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        pytest.param("JAŸ-Z", "Jay-Z", id="diaeresis"),
        pytest.param("Beyoncé", "Beyonce", id="acute_accent"),
        pytest.param("Sigur Rós", "sigur ros", id="accent_and_case"),
        pytest.param("ＡＢＣ", "abc", id="full_width"),
        pytest.param("방탄소년단", "방탄소년단", id="hangul_unchanged"),
    ],
)
def test_clean_str_matches_spellings_of_the_same_name(
    given: str, expected: str
) -> None:
    """Names that differ only in accents, case, punctuation or width compare equal."""
    assert clean_str(given) == clean_str(expected)


def test_clean_str_keeps_distinct_names_distinct() -> None:
    """Removing accents doesn't make different names compare equal."""
    assert clean_str("Jay-Z") != clean_str("Jay Rock")
