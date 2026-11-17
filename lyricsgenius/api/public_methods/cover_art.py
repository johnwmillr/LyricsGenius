from typing import Any

from ...types.types import TextFormatT
from ..protocols import CoverArtsCapable, RequestCapable


class CoverArtMethods(RequestCapable, CoverArtsCapable):
    """Cover art methods of the public API."""

    def cover_arts(
        self,
        song_id: int | None = None,
        album_id: int | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Gets the cover arts of an album.

        Args:
            song_id (:obj:`int`, optional): No longer supported. Genius only
                serves cover arts by album, so passing it raises ``ValueError``.
            album_id (:obj:`int`): Genius album ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain'). Defines the text
                formatting for the annotation of the cover arts,
                if there are any.

        Returns:
            :obj:`dict`

        Raises:
            ValueError: If :obj:`song_id` is passed or :obj:`album_id` is missing.

        """
        if song_id is not None:
            raise ValueError(
                "Genius no longer serves cover arts by song. Pass the album_id of "
                "the song's album instead."
            )
        if album_id is None:
            raise ValueError("Must supply `album_id`.")
        endpoint = "cover_arts"
        params: dict[str, Any] = {
            "album_id": album_id,
            "text_format": text_format or self.response_format,
        }
        return self._make_request(path=endpoint, params_=params, public_api=True)
