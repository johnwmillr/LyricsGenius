"""
Copyright (C) 2022 dopebnan
This file is part of AGenius.py.
You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

import aiohttp
import asyncio


class Sender(object):
    """Sends requests to Genius."""
    API_ROOT = "https://api.genius.com/"

    def __init__(self, access_token, retries=0):
        self.retries = retries
        if not isinstance(access_token, str):
            raise TypeError("Bad token")
        self.headers = {
            "application": "Genius-py",
            "User-Agent": "https://github.com/dopebnan/Genius-py",
            "Authorization": f"Bearer {access_token}"
        }

    async def _make_request(self, path, params_=None, **kwargs):
        """Makes a request to Genius."""
        async with aiohttp.ClientSession(headers=self.headers) as _session:

            uri = self.API_ROOT

            uri += path

            params_ = {} if not params_ else params_

            # Making the request
            response = None
            tries = 0
            while response is None and tries <= self.retries:
                tries += 1
                response = await _session.get(uri, params=params_, **kwargs)
                response.raise_for_status()
                await asyncio.sleep(2)

            if response.status == 200:
                res = await response.json()
                return res["response"]
            elif response.status == 204:
                return 204
            else:
                raise AssertionError(f"Response code is {response.status}")

    async def _make_request_web(self, path):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        async with aiohttp.ClientSession(headers=headers) as _session:

            response = None
            tries = 0
            while response is None and tries <= self.retries:
                tries += 1
                response = await _session.get(path)
                response.raise_for_status()
                await asyncio.sleep(2)

            if response.status == 200:
                res = await response.text()
                return res
            elif response.status == 204:
                return 204
            else:
                raise AssertionError(f"Response code is {response.status}")
