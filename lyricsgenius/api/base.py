import os
import platform
import time
from json.decoder import JSONDecodeError
from typing import Any, Protocol

import requests
from requests.exceptions import HTTPError, RequestException, Timeout

from ..types.types import ResponseFormatT


class Requester(Protocol):
    response_format: ResponseFormatT

    def _make_request(
        self,
        path: str,
        method: str = "GET",
        params_: dict[str, Any] | None = None,
        public_api: bool = False,
        web: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Makes a request to Genius."""
        pass


class Sender(Requester):
    """Sends requests to Genius."""

    # Create a persistent requests connection
    API_ROOT = "https://api.genius.com/"
    PUBLIC_API_ROOT = "https://genius.com/api/"
    WEB_ROOT = "https://genius.com/"

    def __init__(
        self,
        access_token: str | None = None,
        response_format: ResponseFormatT = "plain",
        timeout: int = 5,
        sleep_time: float = 0.2,
        retries: int = 0,
        public_api_constructor: bool = False,
        user_agent: str = "",
        proxy: dict[str, str] | None = None,
    ) -> None:
        self._session = requests.Session()
        user_agent_root = f"{platform.system()} {platform.release()}; Python {platform.python_version()}"
        self._session.headers = {
            "application": "LyricsGenius",
            "User-Agent": f"({user_agent}) ({user_agent_root})"
            if user_agent
            else user_agent_root,
        }
        if proxy:
            self._session.proxies = proxy
        if access_token is None:
            access_token = os.environ["GENIUS_ACCESS_TOKEN"]

        if public_api_constructor:
            self.authorization_header = {}
        else:
            if not access_token or not isinstance(access_token, str):
                raise TypeError("Invalid token")
            self.access_token = "Bearer " + access_token
            self.authorization_header = {"authorization": self.access_token}

        self.response_format = response_format
        self.timeout = timeout
        self.sleep_time = sleep_time
        if retries < 0:
            raise ValueError("retries must be a non-negative integer")
        self.retries = retries

    def _make_request(
        self,
        path: str,
        method: str = "GET",
        params_: dict[str, Any] | None = None,
        public_api: bool = False,
        web: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Makes a request to Genius."""
        header = None
        if public_api:
            uri = self.PUBLIC_API_ROOT
        elif web:
            uri = self.WEB_ROOT
        else:
            uri = self.API_ROOT
            header = self.authorization_header
        uri += path
        params_ = params_ if params_ else {}

        # Make the request
        response = None
        tries = 0
        while response is None and tries <= self.retries:
            tries += 1
            try:
                response = self._session.request(
                    method,
                    uri,
                    timeout=self.timeout,
                    params=params_,
                    headers=header,
                    **kwargs,
                )
            except Timeout as e:
                error = f"Request timed out:\n{e}"
                if tries > self.retries:
                    raise Timeout(error) from e
            except HTTPError as e:
                assert response is not None
                error = get_description(e)
                if response.status_code < 500 or tries > self.retries:
                    raise HTTPError(response.status_code, error) from e

            # Enforce rate limiting
            time.sleep(self.sleep_time)

        if response is None:
            raise RuntimeError("Response is None, something went wrong.")
        if web:
            return {"html": response.text}
        if response.status_code == 200:
            response_data: dict[str, Any] = response.json()
            return response_data.get("response", response_data)
        raise AssertionError(
            f"Unexpected response status code: {response.status_code}. "
            f"Expected 200 or 204. Response body: {response.text}. "
            f"Response headers: {response.headers}."
        )


def get_description(e: RequestException) -> str:
    """Extract a descriptive error message from a RequestException instance."""
    try:
        response = e.response.json() if e.response else {}
    except JSONDecodeError:
        return str(e)

    description = response.get("meta", {}).get("message") or response.get(
        "error_description"
    )

    return f"{e}\n{description}" if description else str(e)
