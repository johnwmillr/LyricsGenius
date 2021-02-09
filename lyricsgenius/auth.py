from urllib.parse import urlencode
import webbrowser

from .utils import parse_redirected_url
from .api import Sender
from .errors import InvalidStateError


class OAuth2(Sender):
    """Genius OAuth2 authorization flow.

    Using this class you can authenticate a user,
    and get their token.

    Args:
        client_id (:obj:`str`): Client ID
        redirect_uri (:obj:`str`): Whitelisted redirect URI.
        client_secret (:obj:`str`, optional): Client secret.
        scope (:obj:`tuple` | :obj:`"all"`, optional): Token privileges.
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
                 client_secret=None, scope=None,
                 state=None, client_only_app=False):
        super().__init__()
        msg = ("You must provide a client_secret "
               "if you intend to use the full code exchange."
               "\nIf you meant to use the client-only flow, "
               "set the client_only_app parameter to True.")
        assert any([client_secret, client_only_app]), msg
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if scope == 'all':
            scope = ('me', 'create_annotation', 'manage_annotation', 'vote')
        self.scope = scope if scope else ()
        self.state = state
        self.flow = 'token' if client_only_app else 'code'
        self.client_only_app = client_only_app

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

    def get_user_token(self, code=None, url=None, state=None, **kwargs):
        """Gets a user token using the url or the code parameter..

        If you supply value for :obj:`code`, this method will use the value of the
        :obj:`code` parameter to request a token from Genius.

        If you use the :method`client_only_app` and supplt the redirected URL,
        it will already have the token.
        You could pass the URL to this method or parse it yourself.

        If you provide a :obj:`state` the method will also compare
        it to the initial state and will raise an exception if
        they're not equal.

        Args:
            code (:obj:`str`): 'code' parameter of redirected URL.
            url (:obj:`str`): Redirected URL (used in client-only apps)
            state (:obj:`str`): state parameter of redirected URL (only
                provide if you want to compare with initial :obj:`self.state`)
            **kwargs: keywords for the POST request.
        returns:
            :obj:`str`: User token.

        """
        assert any([code, url]), "You must pass either `code` or `url`."

        if state is not None and self.state != state:
            raise InvalidStateError('States do not match.')

        if code:
            payload = {'code': code,
                       'client_id': self.client_id,
                       'client_secret': self.client_secret,
                       'redirect_uri': self.redirect_uri,
                       'grant_type': 'authorization_code',
                       'response_type': 'code'}
            url = OAuth2.token_url.replace('https://api.genius.com/', '')
            res = self._make_request(url, 'POST', data=payload, **kwargs)
            token = res['access_token']
        else:
            token = parse_redirected_url(url, self.flow)
        return token

    def prompt_user(self):
        """Prompts current user for authentication.

        Opens a web browser for you to log in with Genius.
        Prompts to paste the URL after logging in to parse the
        *token* URL parameter.

        returns:
            :obj:`str`: User token.

        """

        url = self.url
        print('Opening browser for Genius login...')
        webbrowser.open(url)
        redirected = input('Please paste redirect URL: ').strip()

        if self.flow == 'token':
            token = parse_redirected_url(redirected, self.flow)
        else:
            code = parse_redirected_url(redirected, self.flow)
            token = self.get_user_token(code)

        return token

    @classmethod
    def client_only_app(cls, client_id, redirect_uri, scope=None, state=None):
        """Returns an OAuth2 instance for a client-only app.

        Args:
            client_id (:obj:`str`): Client ID.
            redirect_uri (:obj:`str`): Whitelisted redirect URI.
            scope (:obj:`tuple` | :obj:`"all"`, optional): Token privilages.
            state (:obj:`str`, optional): Request state.

        returns:
            :class:`OAuth2`

        """
        return cls(client_id=client_id,
                   redirect_uri=redirect_uri,
                   scope=scope,
                   state=state,
                   client_only_app=True)

    @classmethod
    def full_code_exchange(cls, client_id, redirect_uri,
                           client_secret, scope=None, state=None):
        """Returns an OAuth2 instance for a full-code exchange app.

        Args:
            client_id (:obj:`str`): Client ID.
            redirect_uri (:obj:`str`): Whitelisted redirect URI.
            client_secret (:obj:`str`): Client secret.
            scope (:obj:`tuple` | :obj:`"all"`, optional): Token privilages.
            state (:obj:`str`, optional): Request state.

        returns:
            :class:`OAuth2`

        """
        return cls(client_id=client_id,
                   client_secret=client_secret,
                   redirect_uri=redirect_uri,
                   scope=scope,
                   state=state)

    def __repr__(self):
        return ("{name}("
                "flow={flow!r}, "
                "scope={scope!r}, "
                "state={state!r}, "
                "client_only_app={client_only_app!r})"
                ).format(
            name=self.__class__.__name__,
            flow=self.flow,
            scope=self.scope,
            state=self.state,
            client_only_app=self.client_only_app
        )
