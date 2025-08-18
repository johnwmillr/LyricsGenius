"""
Protocol definitions for static typing of mixin capabilities.
"""

from typing import Any, Protocol

from ..types.types import ResponseFormatT, TextFormatT


class RequestCapable(Protocol):
    response_format: ResponseFormatT

    def _make_request(
        self,
        path: str,
        method: str = "GET",
        params_: dict[str, Any] | list[tuple[Any, Any]] | None = None,
        public_api: bool = False,
        web: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]: ...


class ChartsCapable(Protocol):
    """Interface for classes that support the .charts(...) method."""

    response_format: ResponseFormatT

    def charts(
        self,
        time_period: str = "day",
        chart_genre: str = "all",
        per_page: int | None = None,
        page: int | None = None,
        text_format: TextFormatT | None = None,
        type_: str = "songs",
    ) -> dict[str, Any]: ...


class CoverArtsCapable(Protocol):
    """Interface for classes that support the .cover_arts(...) method."""

    response_format: ResponseFormatT

    def cover_arts(
        self,
        song_id: int | None = None,
        album_id: int | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]: ...
