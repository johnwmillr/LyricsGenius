from lyricsgenius.utils import parse_redirected_url

from urllib.parse import urlencode
import webbrowser
import requests


class OAuth2(object):
    """Genius OAuth2 authorization flow.

    Using this class you can authenticate a user,
    and get their token.

    Args:
        client_id (:obj:`str`): Client ID
        redirect_uri (:obj:`str`): Whitelisted redirect URI.
        client_secret (:obj:`str`, optional): Client secret.
        scope (:obj:`list` | :obj:`all`, optional) : Token privilages.
        state (:obj:`str`, optional): Request state.
        client_only_app (:obj:`bool`, optional): `True` to use the client-only
            authorization flow, otherwise `False`.

    Raises:
        AssertionError: If neither :obj:`client_secret`, nor
            :obj:`client_only_app` is supplied.

    """
    auth_url = 'https://api.genius.com/oauth/authorize'
    token_url = 'https://api.genius.com/oauth/token'

    def __init__(self, client_id, redirect_uri,
                 client_secret=None, scope=None, state=None, client_only_app=False):

        msg = ("You must provide a client_secret "
               "if you intend to use the normal authorization flow"
               "\nIf you meant to use the client-only flow, "
               "set the client_only_app parameter to True.")
        assert any([client_secret, client_only_app]), msg
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if scope == 'all':
            scope = ('me', 'create_annotation', 'manage_annotation', 'vote')
        self.scope = scope
        self.state = state
        self.flow = 'token' if client_only_app else 'code'

    @property
    def url(self):
        """Returns the URL you redirect the user to.
        You can use this property to get a URL that when opened on the user's
        device, shows Genius's authorization page where user clicks *Agree*
        to give your app access, and then Genius redirects user back to your
        redirect URI.

        """
        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': self.flow
        }
        if self.scope:
            payload['scope'] = ' '.join(self.scope)
        if self.state:
            payload['state'] = self.state
        return OAuth2.auth_url + '?' + urlencode(payload)

    def get_user_token(self, url, **kwargs):
        """Gets a user token using the redirected URL.
        This method will either get the value of the *token*
        parameter in the redirected URL, or use the value of the
        *code* parameter to request a token from Genius.

        Args:
            url (:obj:`str`): 'code' parameter of redirected URL.
            **kwargs: keywords for the POST request.
        returns:
            :obj:`str`: User token.

        """
        if self.flow == 'code':
            payload = {'code': parse_redirected_url(url, self.flow),
                       'client_id': self.client_id,
                       'client_secret': self.client_secret,
                       'redirect_uri': self.redirect_uri,
                       'grant_type': 'authorization_code',
                       'response_type': 'code'}
            res = requests.post(OAuth2.token_url, payload, **kwargs)
            res.raise_for_status()
            return res.json()['access_token']
        elif self.flow == 'token':
            return parse_redirected_url(url, self.flow)

    def prompt_user(self):
        """Prompts current user for authentication.

        Opens a web browser for you to log in with Genius.
        Prompts to paste the URL after logging in to parse the
        *code* or *token* URL parameter.

        returns:
            :obj:`str`: User token.

        """

        url = self.url
        print('Opening browser for Genius login...')
        webbrowser.open(url)
        redirected = input('Please paste redirect URL: ').strip()

        code = parse_redirected_url(redirected, self.flow)
        return code if self.client_only_app else self.get_user_token(code)
