"""Tests for how HTTP errors from Genius are raised, retried and reported."""

import json
import logging
from typing import Any
from unittest import mock

import pytest
import requests
from requests.exceptions import HTTPError, Timeout

from lyricsgenius import Genius

SONG_URL = "https://genius.com/Mocking-the-tests-lyrics"


def _response(
    status_code: int,
    body: str = "",
    content_type: str = "application/json",
    url: str = "https://api.genius.com/",
) -> requests.Response:
    """Builds a requests.Response with the given status and body."""
    response = requests.Response()
    response.status_code = status_code
    response._content = body.encode()
    response.headers["Content-Type"] = content_type
    response.url = url
    response.reason = "Mocked"
    return response


def _json_response(status_code: int, payload: dict[str, Any]) -> requests.Response:
    return _response(status_code, json.dumps(payload))


def _forbidden_page() -> requests.Response:
    return _response(
        403,
        "<html><body>Just a moment...</body></html>",
        content_type="text/html",
        url=SONG_URL,
    )


def _song_hit() -> dict[str, Any]:
    return {
        "index": "song",
        "result": {
            "id": 1,
            "title": "Mocking the Tests",
            "primary_artist": {"name": "Pytest"},
            "lyrics_state": "complete",
            "instrumental": False,
            "url": SONG_URL,
        },
    }


def _patch_request(genius: Genius, **kwargs: Any) -> Any:
    return mock.patch.object(genius._session, "request", **kwargs)


def test_web_request_returns_html_on_success(genius: Genius) -> None:
    """A successful page request returns the page's HTML."""
    page = _response(200, "<html>lyrics</html>", content_type="text/html")
    with _patch_request(genius, return_value=page):
        assert genius._make_request("some-page", web=True) == {
            "html": "<html>lyrics</html>"
        }


def test_web_request_raises_on_403(genius: Genius) -> None:
    """A blocked page request raises HTTPError carrying the response."""
    with _patch_request(genius, return_value=_forbidden_page()):
        with pytest.raises(HTTPError) as exc_info:
            genius._make_request("Mocking-the-tests-lyrics", web=True)

    assert exc_info.value.args[0] == 403
    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code == 403


def test_lyrics_raises_on_403_without_parsing_page(
    genius: Genius, caplog: pytest.LogCaptureFixture
) -> None:
    """A blocked lyrics page raises instead of being parsed as lyrics."""
    with (
        caplog.at_level(logging.WARNING, logger="lyricsgenius"),
        _patch_request(genius, return_value=_forbidden_page()),
        pytest.raises(HTTPError),
    ):
        genius.lyrics(song_url=SONG_URL)

    assert "Couldn't find the lyrics section" not in caplog.text


def test_search_song_raises_on_403_lyrics_page(genius: Genius) -> None:
    """search_song lets a blocked lyrics page's HTTPError through."""
    search_all_response = {"sections": [{"type": "song", "hits": [_song_hit()]}]}
    with (
        mock.patch.object(genius, "search_all", return_value=search_all_response),
        _patch_request(genius, return_value=_forbidden_page()),
        pytest.raises(HTTPError) as exc_info,
    ):
        genius.search_song("Mocking the Tests", get_full_info=False)

    assert exc_info.value.args[0] == 403


def test_api_error_includes_genius_message(genius: Genius) -> None:
    """An API error carries the status code and Genius's error message."""
    not_found = _json_response(404, {"meta": {"status": 404, "message": "Not found"}})
    with _patch_request(genius, return_value=not_found):
        with pytest.raises(HTTPError) as exc_info:
            genius.song(1)

    assert exc_info.value.args[0] == 404
    assert "Not found" in exc_info.value.args[1]


def test_request_does_not_retry_client_errors() -> None:
    """A 4xx response raises at once, without retrying."""
    genius = Genius("dummy_access_token", sleep_time=0, retries=2)
    not_found = _json_response(404, {"meta": {"status": 404}})
    with _patch_request(genius, return_value=not_found) as request:
        with pytest.raises(HTTPError):
            genius.song(1)

    assert request.call_count == 1


def test_request_retries_server_errors() -> None:
    """A 5xx response is retried and a later success is returned."""
    genius = Genius("dummy_access_token", sleep_time=0, retries=2)
    responses = [
        _json_response(500, {}),
        _json_response(200, {"response": {"song": {"id": 1}}}),
    ]
    with _patch_request(genius, side_effect=responses) as request:
        assert genius.song(1) == {"song": {"id": 1}}

    assert request.call_count == 2


def test_request_raises_server_error_after_retries() -> None:
    """A 5xx response that persists raises once retries run out."""
    genius = Genius("dummy_access_token", sleep_time=0, retries=1)
    responses = [_json_response(503, {}), _json_response(503, {})]
    with _patch_request(genius, side_effect=responses) as request:
        with pytest.raises(HTTPError) as exc_info:
            genius.song(1)

    assert exc_info.value.args[0] == 503
    assert request.call_count == 2


def test_request_returns_empty_dict_for_no_content(genius: Genius) -> None:
    """A 204 response returns an empty dict."""
    with _patch_request(genius, return_value=_response(204)):
        assert genius._make_request("annotations/1", method="DELETE") == {}


def test_delete_annotation_returns_204(genius: Genius) -> None:
    """Deleting an annotation returns 204 on success."""
    with _patch_request(genius, return_value=_response(204)):
        assert genius.delete_annotation(1) == 204


def test_delete_annotation_raises_on_error(genius: Genius) -> None:
    """A failed annotation deletion raises HTTPError."""
    forbidden = _json_response(403, {"meta": {"status": 403}})
    with _patch_request(genius, return_value=forbidden):
        with pytest.raises(HTTPError):
            genius.delete_annotation(1)


def _client(**kwargs: Any) -> Genius:
    """Builds a Genius client with a known dummy token and no delay."""
    return Genius("dummy_access_token", sleep_time=0, **kwargs)


def test_api_request_sends_authorization_header() -> None:
    """Official API requests carry the access token."""
    genius = _client()
    ok = _json_response(200, {"response": {"song": {}}})

    with _patch_request(genius, return_value=ok) as request:
        genius.song(1)

    assert request.call_args.kwargs["headers"] == {
        "authorization": "Bearer dummy_access_token"
    }


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({"public_api": True}, id="public_api"),
        pytest.param({"web": True}, id="web_page"),
    ],
)
def test_public_and_web_requests_omit_authorization(kwargs: dict[str, bool]) -> None:
    """Requests to genius.com never carry the access token."""
    genius = _client()
    ok = _response(200, "{}", content_type="text/html")

    with _patch_request(genius, return_value=ok) as request:
        genius._make_request("some-path", **kwargs)

    assert request.call_args.kwargs["headers"] is None


def test_request_retries_timeouts() -> None:
    """A timed-out request is retried and a later success is returned."""
    genius = _client(retries=1)
    ok = _json_response(200, {"response": {"song": {"id": 1}}})

    with _patch_request(genius, side_effect=[Timeout(), ok]) as request:
        assert genius.song(1) == {"song": {"id": 1}}

    assert request.call_count == 2


def test_request_raises_timeout_after_retries() -> None:
    """A request that keeps timing out raises Timeout once retries run out."""
    genius = _client(retries=1)

    with _patch_request(genius, side_effect=[Timeout(), Timeout()]) as request:
        with pytest.raises(Timeout, match="timed out"):
            genius.song(1)

    assert request.call_count == 2


def test_request_waits_sleep_time_after_each_request() -> None:
    """Each request is followed by a pause of sleep_time seconds."""
    genius = Genius("dummy_access_token", sleep_time=0.25, retries=1)
    responses = [_json_response(500, {}), _json_response(200, {"response": {}})]

    with (
        _patch_request(genius, side_effect=responses),
        mock.patch("lyricsgenius.api.base.time.sleep") as sleep,
    ):
        genius.song(1)

    assert sleep.call_args_list == [mock.call(0.25), mock.call(0.25)]


def test_genius_rejects_negative_retries() -> None:
    """A negative retry count is rejected."""
    with pytest.raises(ValueError, match="retries"):
        _client(retries=-1)
