import os
import unittest
from urllib.parse import urlparse
from unittest.mock import MagicMock, patch

from lyricsgenius import OAuth2

client_id = os.environ["GENIUS_CLIENT_ID"]
client_secret = os.environ["GENIUS_CLIENT_SECRET"]
redirect_uri = os.environ["GENIUS_REDIRECT_URI"]


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code > 300:
                raise ConnectionError

    method, url = args[0], args[1]
    data = kwargs['data']
    code = data.get('code')
    data_client_id = data.get('client_id')
    data_client_secret = data.get('client_secret')
    data_redirect_uri = data.get('redirect_uri')
    grant_type = data.get('grant_type')
    response_type = data.get('response_type')

    if (method == 'POST'
        and url == OAuth2.token_url
        and code == 'some_code'
        and data_client_id == client_id
        and data_client_secret == client_secret
        and data_redirect_uri == redirect_uri
        and grant_type == 'authorization_code'
            and response_type == 'code'):
        return MockResponse({"access_token": "test"}, 200)

    return MockResponse(None, 403)


def patch_request():
    patch('lyricsgenius.api.base.Sender._session.request',
          side_effect=mocked_requests_post)


class TestOAuth2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up OAuth2 tests...\n")

    def test_init(self):
        with self.assertRaises(AssertionError):
            OAuth2(client_id, redirect_uri)

        scope = ('me', 'create_annotation', 'manage_annotation', 'vote')
        auth = OAuth2(client_id, redirect_uri,
                      client_secret, scope='all')
        self.assertEqual(auth.scope, scope)

    def test_url_client_flow(self):
        token_flow_url = ('https://api.genius.com/oauth/authorize?'
                          'client_id=' + client_id + ''
                          '&redirect_uri=' + urlparse(redirect_uri) + ''
                          '&response_type=token'
                          '&scope=me+create_annotation+manage_annotation+vote'
                          )
        auth = OAuth2(client_id, redirect_uri,
                      scope='all', client_only_app=True)

        self.assertEqual(token_flow_url, auth.url)

    def test_url_code_flow(self):
        code_flow_url = ('https://api.genius.com/oauth/authorize?'
                         'client_id=' + client_id + ''
                         '&redirect_uri=' + urlparse(redirect_uri) + ''
                         '&response_type=code'
                         '&scope=me+create_annotation+manage_annotation+vote'
                         )
        auth = OAuth2(client_id, redirect_uri,
                      client_secret, scope='all')

        self.assertEqual(code_flow_url, auth.url)

    def test_get_user_token_client_flow(self):
        # client-only flow
        auth = OAuth2(client_id, redirect_uri, client_only_app=True)
        redirected = 'https://example.com/callback#access_token=test'
        client_flow_token = 'test'

        r = auth.get_user_token(redirected)
        self.assertEqual(r, client_flow_token)

    @patch('lyricsgenius.api.base.Sender._session.request',
           side_effect=mocked_requests_post)
    def test_get_user_token_code_flow(self, mock_post):
        # full code exchange flow
        auth = OAuth2(client_id, redirect_uri,
                      client_secret, scope='all')
        redirected = 'https://example.com/callback?code=some_code'
        code_flow_token = 'test'

        r = auth.get_user_token(redirected)
        self.assertEqual(r, code_flow_token)

    def test_prompt_user(self):
        auth = OAuth2(client_id, redirect_uri,
                      client_secret, scope='all')
        token = 'test'
        current_module = 'lyricsgenius.auth'

        input_ = MagicMock(return_value='http://example.com?code=some_code')
        with patch(current_module + '.webbrowser', MagicMock()), \
            patch(current_module + '.input', input_), \
            patch(current_module + '.print', MagicMock()), \
            patch('lyricsgenius.api.base.Sender._session.request',
                  side_effect=mocked_requests_post):
            r = auth.prompt_user()

        self.assertEqual(r, token)
