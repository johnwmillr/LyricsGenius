import requests
from requests.exceptions import Timeout
import time


class Sender(object):
    """Sends requests to Genius."""
    # Create a persistent requests connection
    _session = requests.Session()
    _session.headers = {'application': 'LyricsGenius',
                        'User-Agent': 'https://github.com/johnwmillr/LyricsGenius'}
    _SLEEP_MIN = 0.2  # Enforce minimum wait time between API calls (seconds)
    API_ROOT = 'https://api.genius.com/'
    PUBLIC_API_ROOT = 'https://genius.com/api/'

    def __init__(
        self,
        client_access_token=None,
        response_format='plain',
        timeout=5,
        sleep_time=0.5
    ):
        if client_access_token is not None:
            self._ACCESS_TOKEN = client_access_token
            self._session.headers['authorization'] = 'Bearer ' + self._ACCESS_TOKEN
        self.response_format = response_format.lower()
        self.timeout = timeout
        self.sleep_time = sleep_time

    def _make_request(self, path, method='GET', params_=None, public_api=False):
        """Makes a request to the API."""
        if public_api:
            uri = self.PUBLIC_API_ROOT
            header = self._session.headers.pop('authorization', None)
        else:
            uri = self.API_ROOT
            header = None
        uri += path

        params_ = params_ if params_ else {}

        # Make the request
        response = None
        try:
            response = self._session.request(method, uri,
                                             timeout=self.timeout,
                                             params=params_)
        except Timeout as e:
            print("Timeout raised and caught:\n{e}".format(e=e))

        if header:
            self._session.headers['authorization'] = header

        # Enforce rate limiting
        time.sleep(max(self._SLEEP_MIN, self.sleep_time))
        return response.json()['response'] if response else None
