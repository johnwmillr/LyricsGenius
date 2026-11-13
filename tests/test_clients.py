"""Tests for constructing the Genius and PublicAPI clients."""

import pytest

from lyricsgenius import Genius, PublicAPI
from lyricsgenius.api import API


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


SHADOWED_NAMES = [
    "annotation",
    "artist",
    "artist_songs",
    "referents",
    "search_songs",
    "song",
]


@pytest.mark.parametrize("name", SHADOWED_NAMES)
def test_genius_uses_official_api_for_shared_names(name: str) -> None:
    """Names defined by both APIs resolve to the official API on Genius."""
    assert getattr(Genius, name) is getattr(API, name)
    assert getattr(Genius, name) is not getattr(PublicAPI, name)


def test_shadowed_names_are_exactly_the_shared_ones() -> None:
    """Only the listed names are defined by both APIs, so none go unnoticed."""

    def public_methods(cls: type) -> set[str]:
        return {
            name
            for name, value in vars(cls).items()
            if callable(value) and not name.startswith("_")
        }

    public_api_methods = set().union(
        *(public_methods(base) for base in PublicAPI.__mro__)
    )
    assert public_methods(API) & public_api_methods == set(SHADOWED_NAMES)
