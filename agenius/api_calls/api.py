"""
Copyright (C) 2022 dopebnan
This file is part of AGenius.py.
You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

from .base import Sender


class API(Sender):
    def __init__(self, access_token, retries=0):
        """
        Genius API.

        The :obj:`API` class is in charge of making all the requests to the developers' API (api.genius.com).

        :param access_token: str, API key provided by Genius
        :param retries: int, number of retries in case of timeouts;
            default: 0, requests are only made once
        """
        super().__init__(access_token=access_token, retries=retries)

    async def account(self, text_format='plain'):
        """
        Gets details about the current user.

        Requires scope: 'me'

        :param text_format: str, text format of the results ('dom', 'html', 'markdown' or 'plain');
            default: 'plain'

        :return: dict
        """
        endpoint = "account"
        params = {"text_format": text_format}
        return await self._make_request(path=endpoint, params_=params)

    async def annotation(self, annotation_id, text_format='plain'):
        """
        Gets data for a specific annotation.

        :param annotation_id: int, annotation ID
        :param text_format: str, text format of the results ('dom', 'html', 'markdown' or 'plain');
            default: 'plain'
        :return: dict
        """
        params = {"text_format": text_format}
        endpoint = f"annotations/{annotation_id}"
        return await self._make_request(endpoint, params_=params)

    async def artist(self, artist_id, text_format='plain'):
        """
        Gets data for a specific artist.

        :param artist_id: int, Genius artist ID
        :param text_format: str, text format of the results ('dom', 'html', 'markdown' or 'plain');
            default: 'plain'
        :return: dict
        """
        params = {"text_format": text_format}
        endpoint = f"artists{artist_id}"
        return await self._make_request(endpoint, params_=params)

    async def artist_songs(self, artist_id, per_page, sort):
        """
        Gets the specified artist's songs

        :param artist_id: int, Genius artist ID
        :param per_page: int, number of results to return (it can't be more than 50)
        :param sort: str, sorting preference ('title', 'popularity', 'release_date')

        :return: dict
        """
        endpoint = f"artists/{artist_id}/songs"
        params = {
            "sort": sort,
            "per_page": per_page,
            "page": 0
        }
        return await self._make_request(endpoint, params_=params)

    async def search(self, search_term, per_page):
        """
        Searches on Genius.

        :param search_term: str, a term to search for on Genius
        :param per_page: int, number of results per page (has to be less than 5)

        :return: dict
        """
        endpoint = "search"
        params = {
            'q': search_term,
            "per_page": per_page,
            "page": 0
        }
        return await self._make_request(endpoint, params_=params)

    async def song(self, song_id, text_format='plain'):
        """
        Gets data for a specific song.

        :param song_id: int, Genius song ID
        :param text_format: str, text format of the results ('dom', 'html', 'markdown' or 'plain');
            default: 'plain'

        :return: dict
        """
        endpoint = f"songs/{song_id}"
        params = {"text_format": text_format}
        return await self._make_request(endpoint, params_=params)
