"""Tests for constructing the Genius and PublicAPI clients."""

import pytest

from lyricsgenius import Genius, PublicAPI


def test_public_api_does_not_need_a_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """PublicAPI can be created without a token or GENIUS_ACCESS_TOKEN."""
    monkeypatch.delenv("GENIUS_ACCESS_TOKEN", raising=False)

    client = PublicAPI()

    assert client.authorization_header == {}


def test_genius_reads_token_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Genius falls back to GENIUS_ACCESS_TOKEN when no token is passed."""
    monkeypatch.setenv("GENIUS_ACCESS_TOKEN", "env_token")

    client = Genius()

    assert client.authorization_header == {"authorization": "Bearer env_token"}


def test_genius_requires_a_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Genius raises when no token is passed and GENIUS_ACCESS_TOKEN is unset."""
    monkeypatch.delenv("GENIUS_ACCESS_TOKEN", raising=False)

    with pytest.raises(KeyError, match="GENIUS_ACCESS_TOKEN"):
        Genius()
