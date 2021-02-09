import os
import unittest
from unittest.mock import MagicMock, patch


from lyricsgenius import OAuth2
from lyricsgenius.errors import InvalidStateError

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
    data_grant_type = data.get('grant_type')
    data_response_type = data.get('response_type')

    if (method == 'POST'
        and url == OAuth2.token_url
        and code == 'some_code'
        and data_client_id == client_id
        and data_client_secret == client_secret
        and data_redirect_uri == redirect_uri
        and data_grant_type == 'authorization_code'
            and data_response_type == 'code'):
        return MockResponse({"access_token": "test"}, 200)

    return MockResponse(None, 403)


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

    @patch('requests.Session.request',
           side_effect=mocked_requests_post)
    def test_get_user_token_code_flow(self, mock_post):
        # full code exchange flow

        state = 'some_state'
        code = 'some_code'
        code_flow_token = 'test'

        auth = OAuth2.full_code_exchange(
            client_id,
            redirect_uri,
            client_secret,
            scope='all',
            state=state
        )

        r = auth.get_user_token(code=code, state=state)
        self.assertEqual(r, code_flow_token)

    def test_get_user_token_token_flow(self):

        state = 'some_state'
        token_flow_token = 'test'
        redirected_url = '{}#access_token=test'.format(redirect_uri)

        auth = OAuth2.client_only_app(
            client_id,
            redirect_uri,
            scope='all',
            state=state
        )

        r = auth.get_user_token(url=redirected_url)
        self.assertEqual(r, token_flow_token)

    def test_get_user_token_invalid_state(self):
        state = 'state_1'
        auth = OAuth2.full_code_exchange(
            client_id,
            redirect_uri,
            client_secret,
            scope='all',
            state=state
        )

        returned_code = 'some_code'
        returned_state = 'state_2'
        with self.assertRaises(InvalidStateError):
            auth.get_user_token(code=returned_code, state=returned_state)

    def test_get_user_token_no_parameter(self):
        state = 'some_state'
        auth = OAuth2.full_code_exchange(
            client_id,
            redirect_uri,
            client_secret,
            scope='all',
            state=state
        )

        with self.assertRaises(AssertionError):
            auth.get_user_token()

    def test_prompt_user(self):
        auth = OAuth2(client_id, redirect_uri,
                      client_secret, scope='all')
        token = 'test'
        current_module = 'lyricsgenius.auth'

        input_ = MagicMock(return_value='http://example.com?code=some_code')
        with patch(current_module + '.webbrowser', MagicMock()), \
            patch(current_module + '.input', input_), \
            patch(current_module + '.print', MagicMock()), \
            patch('requests.Session.request',
                  side_effect=mocked_requests_post):
            r = auth.prompt_user()

        self.assertEqual(r, token)
