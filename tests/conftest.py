"""Shared fixtures, options and recording configuration for the test suite."""

import os
from typing import Any

import pytest

from lyricsgenius import Genius, PublicAPI

# Response headers kept in recorded cassettes. Everything else (cookies,
# Cloudflare and tracing headers) is dropped.
_KEPT_RESPONSE_HEADERS = {"content-type"}


def pytest_addoption(parser: pytest.Parser) -> None:
    """Adds the --live option for tests that make real requests to Genius."""
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="run tests marked live, which make real requests to Genius",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Skips live tests unless --live is given."""
    if config.getoption("--live"):
        return
    skip_live = pytest.mark.skip(reason="live test; run with --live")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


def _refuse_lyrics_pages(request: Any) -> Any:
    """Stops a cassette from recording a lyrics page, which holds real lyrics."""
    if request.host == "genius.com" and request.path.endswith("-lyrics"):
        raise RuntimeError(
            f"Refusing to record {request.uri}: cassettes must not contain "
            "real lyrics. Use an invented page in tests/fixtures or mark the "
            "test live."
        )
    return request


def _strip_response_headers(response: dict[str, Any]) -> dict[str, Any]:
    """Drops response headers other than the content type."""
    response["headers"] = {
        name: value
        for name, value in response["headers"].items()
        if name.lower() in _KEPT_RESPONSE_HEADERS
    }
    return response


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Any]:
    """Configures cassettes to omit credentials, cookies and machine details."""
    return {
        "filter_headers": ["authorization", "cookie", "user-agent"],
        "before_record_request": _refuse_lyrics_pages,
        "before_record_response": _strip_response_headers,
        "decode_compressed_response": True,
    }


def _recording(config: pytest.Config) -> bool:
    """Reports whether cassettes are being recorded; the default replays them."""
    return config.getoption("--record-mode") not in (None, "none")


def _sleep_time(config: pytest.Config) -> float:
    """Waits between requests only when they reach Genius."""
    return 0.5 if _recording(config) or config.getoption("--live") else 0


@pytest.fixture
def genius(request: pytest.FixtureRequest) -> Genius:
    """Provides a Genius client for tests that replay or record API responses.

    Replaying needs no token. Recording uses GENIUS_ACCESS_TOKEN, which the
    cassettes never store.
    """
    token = os.environ.get("GENIUS_ACCESS_TOKEN")
    if token is None:
        if _recording(request.config):
            pytest.fail("Recording cassettes requires GENIUS_ACCESS_TOKEN.")
        token = "dummy_access_token"
    return Genius(token, sleep_time=_sleep_time(request.config), timeout=15)


@pytest.fixture
def public_api(request: pytest.FixtureRequest) -> PublicAPI:
    """Provides a PublicAPI client for tests that replay or record responses."""
    return PublicAPI(sleep_time=_sleep_time(request.config), timeout=15)


@pytest.fixture
def live_genius(request: pytest.FixtureRequest) -> Genius:
    """Provides a Genius client that makes real requests, for live tests."""
    token = os.environ.get("GENIUS_ACCESS_TOKEN")
    if token is None:
        pytest.skip("live tests require GENIUS_ACCESS_TOKEN")
    return Genius(token, sleep_time=_sleep_time(request.config), timeout=15)
