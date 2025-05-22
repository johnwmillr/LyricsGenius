from typing import Any

from ...types.types import TextFormatT
from ..protocols import RequestCapable


class DiscussionMethods(RequestCapable):
    """Discussion methods of the public API."""

    def discussion(
        self, discussion_id: int, text_format: TextFormatT | None = None
    ) -> dict[str, Any]:
        """Gets data for a specific discussion.

        Args:
            discussion_id (:obj:`int`): Genius discussion ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Note:
            This request returns a 403 error and will raise ``NotImplementedError``.

        """
        raise NotImplementedError("This request returns a 403 error.")

        endpoint = "discussions/{}".format(discussion_id)  # type: ignore
        params = {"text_format": text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def discussions(self, page: int | None = None) -> dict[str, Any]:
        """Gets discussions.

        Args:
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """

        endpoint = "discussions"
        params = {"page": page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def discussion_replies(
        self,
        discussion_id: int,
        per_page: int | None = None,
        page: int | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Gets the replies on a discussion.

        Args:
            discussion_id (:obj:`int`): Genius discussion ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Note:
            This request returns a 403 error and will raise ``NotImplementedError``.

        """
        raise NotImplementedError("This request returns a 403 error.")

        endpoint = "discussions/{}/forum_posts".format(discussion_id)  # type: ignore
        params = {
            "per_page": per_page,
            "page": page,
            "text_format": text_format or self.response_format,
        }
        return self._make_request(path=endpoint, params_=params, public_api=True)
