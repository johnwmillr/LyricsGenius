"""Tests for the OAuth2 flows, with token requests mocked."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from lyricsgenius import OAuth2
from lyricsgenius.errors import InvalidStateError

CLIENT_ID = "test_client_id"
CLIENT_SECRET = "test_client_secret"
REDIRECT_URI = "http://example.com/callback"
ALL_SCOPES = ("me", "create_annotation", "manage_annotation", "vote")


class _MockResponse:
    """A minimal stand-in for requests.Response."""

    def __init__(self, json_data: dict[str, Any] | None, status_code: int) -> None:
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> dict[str, Any] | None:
        return self.json_data

    def raise_for_status(self) -> None:
        if self.status_code > 300:
            raise ConnectionError


def _mocked_token_request(method: str, url: str, **kwargs: Any) -> _MockResponse:
    """Returns a token only for a well-formed authorization code exchange."""
    data = kwargs["data"]
    if (
        method == "POST"
        and url == OAuth2.token_url
        and data.get("code") == "some_code"
        and data.get("client_id") == CLIENT_ID
        and data.get("client_secret") == CLIENT_SECRET
        and data.get("redirect_uri") == REDIRECT_URI
        and data.get("grant_type") == "authorization_code"
        and data.get("response_type") == "code"
    ):
        return _MockResponse({"access_token": "test"}, 200)
    return _MockResponse(None, 403)


def test_init_requires_client_secret_for_code_flow() -> None:
    """The code flow can't be set up without a client secret."""
    with pytest.raises(AssertionError):
        OAuth2(CLIENT_ID, REDIRECT_URI)


def test_init_expands_all_scope() -> None:
    """The 'all' scope expands to every scope Genius offers."""
    auth = OAuth2(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, scope="all")

    assert auth.scope == ALL_SCOPES


def test_get_user_token_exchanges_code_for_token() -> None:
    """Exchanging an authorization code returns the access token."""
    state = "some_state"
    auth = OAuth2.full_code_exchange(
        CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, scope="all", state=state
    )

    with patch("requests.Session.request", side_effect=_mocked_token_request):
        token = auth.get_user_token(code="some_code", state=state)

    assert token == "test"


def test_get_user_token_reads_token_from_redirect_url() -> None:
    """In the token flow, the token is read from the redirect URL."""
    state = "some_state"
    auth = OAuth2.client_only_app(CLIENT_ID, REDIRECT_URI, scope="all", state=state)

    token = auth.get_user_token(url=f"{REDIRECT_URI}#access_token=test")

    assert token == "test"


def test_get_user_token_rejects_mismatched_state() -> None:
    """A state that doesn't match the one sent raises InvalidStateError."""
    auth = OAuth2.full_code_exchange(
        CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, scope="all", state="state_1"
    )

    with pytest.raises(InvalidStateError):
        auth.get_user_token(code="some_code", state="state_2")


def test_get_user_token_requires_code_or_url() -> None:
    """Getting a token needs a code or a redirect URL."""
    auth = OAuth2.full_code_exchange(
        CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, scope="all", state="some_state"
    )

    with pytest.raises(ValueError, match="code"):
        auth.get_user_token()


def test_prompt_user_exchanges_pasted_code_for_token() -> None:
    """Prompting the user exchanges the code they paste for a token."""
    auth = OAuth2(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, scope="all")
    module = "lyricsgenius.auth"
    input_ = MagicMock(return_value="http://example.com?code=some_code")

    with (
        patch(f"{module}.webbrowser", MagicMock()),
        patch(f"{module}.input", input_, create=True),
        patch(f"{module}.print", MagicMock(), create=True),
        patch("requests.Session.request", side_effect=_mocked_token_request),
    ):
        token = auth.prompt_user()

    assert token == "test"
