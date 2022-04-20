"""
Copyright (C) 2022 dopebnan
This file is part of AGenius.py.
You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

from urllib.parse import urlencode

from api_calls import Sender


class OAuth2(Sender):
    auth_url = "https://api.genius.com/oauth/authorize"
    token_url = "https://api.genius.com/oauth/token"

    def __init__(self, client_id, redirect_uri, client_secret, scope, state):
        """
        Genius OAuth2 authorization flow.

        Using this class you can authenticate a user, and get their token.

        :param client_id: str, client ID
        :param redirect_uri: str, whitelisted redirect URI
        :param client_secret: str, client secret
        :param scope: tuple, token privileges
        :param state: str, request state
        """
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope or ()
        self.state = state
        self.flow = "code"

    @property
    def url(self):
        """
        This url redirects to the Genius authorization page.

        :return:
        """
        payload = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.flow
        }
        if self.scope:
            payload["scope"] = ' '.join(self.scope)
        if self.state:
            payload["state"] = self.state
        return OAuth2.auth_url + '?' + urlencode(payload)

    @classmethod
    def client_only_app(cls, client_id, redirect_uri, scope=None, state=None):
        """
        :param client_id: str, client ID
        :param redirect_uri: str, whitelisted redirect URI
        :param scope: tuple, token privileges
        :param state: str, request state
        :return: OAuth2, OAuth2 instance of a client-only app.
        """
        return cls(client_id=client_id,
                   redirect_uri=redirect_uri,
                   scope=scope,
                   state=state
                   )

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"flow={self.flow!r}"
                f"scope={self.scope!r}"
                f"state={self.state!r}"
                )
