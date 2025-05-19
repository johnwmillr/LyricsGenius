from typing import Any

from ...types.types import TextFormatT
from ..protocols import RequestCapable


class SongMethods(RequestCapable):
    """Song methods of the public API."""

    def song(
        self, song_id: int, text_format: TextFormatT | None = None
    ) -> dict[str, Any]:
        """Gets data for a specific song.

        Args:
            song_id (:obj:`int`): Genius song ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = "songs/{}".format(song_id)
        params = {"text_format": text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def song_activity(
        self,
        song_id: int,
        per_page: int | None = None,
        page: int | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Gets activities on a song.

        Args:
            song_id (:obj:`int`): Genius song ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = "songs/{}/activity_stream/line_items".format(song_id)
        params = {
            "text_format": text_format or self.response_format,
            "per_page": per_page,
            "page": page,
        }
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def song_comments(
        self,
        song_id: int,
        per_page: int | None = None,
        page: int | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Gets the comments on a song.

        Args:
            song_id (:obj:`int`): Genius song ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = "songs/{}/comments".format(song_id)
        params = {
            "per_page": per_page,
            "page": page,
            "text_format": text_format or self.response_format,
        }
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def song_contributors(self, song_id: int) -> dict[str, Any]:
        """Gets the contributors of a song.

        This method will return users who have contributed
        to this song by editing lyrics or song details.

        Args:
            song_id (:obj:`int`): Genius song ID

        Returns:
            :obj:`dict`

        """
        endpoint = "songs/{}/contributors".format(song_id)
        return self._make_request(path=endpoint, public_api=True)
