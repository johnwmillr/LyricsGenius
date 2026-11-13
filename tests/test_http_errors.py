import json
import logging
from typing import Any
from unittest import mock

import pytest
import requests
from requests.exceptions import HTTPError

from lyricsgenius import Genius

SONG_URL = "https://genius.com/Mocking-the-tests-lyrics"


def _response(
    status_code: int,
    body: str = "",
    content_type: str = "application/json",
    url: str = "https://api.genius.com/",
) -> requests.Response:
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


@pytest.fixture
def genius() -> Genius:
    return Genius("dummy_access_token", sleep_time=0)


def _patch_request(genius: Genius, **kwargs: Any) -> Any:
    return mock.patch.object(genius._session, "request", **kwargs)


def test_web_request_returns_html_on_success(genius: Genius) -> None:
    page = _response(200, "<html>lyrics</html>", content_type="text/html")
    with _patch_request(genius, return_value=page):
        assert genius._make_request("some-page", web=True) == {
            "html": "<html>lyrics</html>"
        }


def test_web_request_raises_on_403(genius: Genius) -> None:
    with _patch_request(genius, return_value=_forbidden_page()):
        with pytest.raises(HTTPError) as exc_info:
            genius._make_request("Mocking-the-tests-lyrics", web=True)

    assert exc_info.value.args[0] == 403
    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code == 403


def test_lyrics_raises_on_403_without_parsing_page(
    genius: Genius, caplog: pytest.LogCaptureFixture
) -> None:
    with (
        caplog.at_level(logging.WARNING, logger="lyricsgenius"),
        _patch_request(genius, return_value=_forbidden_page()),
        pytest.raises(HTTPError),
    ):
        genius.lyrics(song_url=SONG_URL)

    assert "Couldn't find the lyrics section" not in caplog.text


def test_search_song_raises_on_403_lyrics_page(genius: Genius) -> None:
    search_all_response = {"sections": [{"type": "song", "hits": [_song_hit()]}]}
    with (
        mock.patch.object(genius, "search_all", return_value=search_all_response),
        _patch_request(genius, return_value=_forbidden_page()),
        pytest.raises(HTTPError) as exc_info,
    ):
        genius.search_song("Mocking the Tests", get_full_info=False)

    assert exc_info.value.args[0] == 403


def test_api_error_includes_description(genius: Genius) -> None:
    not_found = _json_response(404, {"meta": {"status": 404, "message": "Not found"}})
    with _patch_request(genius, return_value=not_found):
        with pytest.raises(HTTPError) as exc_info:
            genius.song(1)

    assert exc_info.value.args[0] == 404
    assert "Not found" in exc_info.value.args[1]


def test_client_errors_are_not_retried() -> None:
    genius = Genius("dummy_access_token", sleep_time=0, retries=2)
    not_found = _json_response(404, {"meta": {"status": 404}})
    with _patch_request(genius, return_value=not_found) as request:
        with pytest.raises(HTTPError):
            genius.song(1)

    assert request.call_count == 1


def test_server_errors_are_retried() -> None:
    genius = Genius("dummy_access_token", sleep_time=0, retries=2)
    responses = [
        _json_response(500, {}),
        _json_response(200, {"response": {"song": {"id": 1}}}),
    ]
    with _patch_request(genius, side_effect=responses) as request:
        assert genius.song(1) == {"song": {"id": 1}}

    assert request.call_count == 2


def test_server_error_raises_after_retries_are_exhausted() -> None:
    genius = Genius("dummy_access_token", sleep_time=0, retries=1)
    responses = [_json_response(503, {}), _json_response(503, {})]
    with _patch_request(genius, side_effect=responses) as request:
        with pytest.raises(HTTPError) as exc_info:
            genius.song(1)

    assert exc_info.value.args[0] == 503
    assert request.call_count == 2


def test_no_content_response_returns_status_code(genius: Genius) -> None:
    with _patch_request(genius, return_value=_response(204)):
        assert genius.delete_annotation(1) == 204
