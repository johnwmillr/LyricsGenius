import time
import os

import requests
from requests.exceptions import HTTPError, Timeout


class Sender(object):
    """Sends requests to Genius."""
    # Create a persistent requests connection
    _SLEEP_MIN = 0.2  # Enforce minimum wait time between API calls (seconds)
    API_ROOT = 'https://api.genius.com/'
    PUBLIC_API_ROOT = 'https://genius.com/api/'

    def __init__(
        self,
        access_token=None,
        response_format='plain',
        timeout=5,
        sleep_time=0.5,
        retries=0
    ):
        self._session = requests.Session()
        self._session.headers = {
            'application': 'LyricsGenius',
            'User-Agent': 'https://github.com/johnwmillr/LyricsGenius'
        }
        if access_token is None:
            access_token = os.environ.get('GENIUS_ACCESS_TOKEN')
        self.access_token = 'Bearer ' + access_token if access_token else None
        self.response_format = response_format.lower()
        self.timeout = timeout
        self.sleep_time = max(self._SLEEP_MIN, sleep_time)
        self.retries = retries

    def _make_request(
        self,
        path,
        method='GET',
        params_=None,
        public_api=False,
        **kwargs
    ):
        """Makes a request to the API."""
        if public_api:
            uri = self.PUBLIC_API_ROOT
            header = None
        else:
            uri = self.API_ROOT
            header = {'authorization': self.access_token}
        uri += path

        params_ = params_ if params_ else {}

        # Make the request
        response = None
        tries = 0
        while response is None and tries <= self.retries:
            tries += 1
            try:
                response = self._session.request(method, uri,
                                                 timeout=self.timeout,
                                                 params=params_,
                                                 headers=header,
                                                 **kwargs)
                response.raise_for_status()
            except Timeout as e:
                error = "Request timed out:\n{e}".format(e=e)
                if tries > self.retries:
                    raise Timeout(error)
            except HTTPError as e:
                error = get_description(e)
                if response.status_code < 500 or tries > self.retries:
                    raise HTTPError(response.status_code, error)

            # Enforce rate limiting
            time.sleep(self.sleep_time)

        if response.status_code == 200:
            res = response.json()
            return res.get("response", res)
        elif response.status_code == 204:
            return 204
        else:
            raise AssertionError("Response status code was neither 200, nor 204! "
                                 "It was {}".format(response.status_code))


def get_description(e):
    error = str(e)
    res = e.response.json()
    description = (res['meta']['message']
                   if res.get('meta')
                   else res.get('error_description'))
    error += '\n{}'.format(description) if description else ''
    return error
