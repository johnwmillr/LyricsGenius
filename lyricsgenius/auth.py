import webbrowser
from typing import Any, ClassVar, Self
from urllib.parse import urlencode

from .api.base import Sender
from .errors import InvalidStateError
from .types.types import ScopeT
from .utils import parse_redirected_url


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

    auth_url: ClassVar[str] = "https://api.genius.com/oauth/authorize"
    token_url: ClassVar[str] = "https://api.genius.com/oauth/token"
    scope: ScopeT

    def __init__(
        self,
        client_id: str,
        redirect_uri: str,
        client_secret: str | None = None,
        scope: ScopeT | None = None,
        state: str | None = None,
        app_is_client_only: bool = False,
    ) -> None:
        super().__init__()
        msg = (
            "You must provide a client_secret "
            "if you intend to use the full code exchange."
            "\nIf you meant to use the client-only flow, "
            "set the app_is_client_only parameter to True."
        )
        assert any([client_secret, app_is_client_only]), msg
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if scope == "all":
            self.scope = ("me", "create_annotation", "manage_annotation", "vote")
        elif isinstance(scope, tuple):
            self.scope = scope
        elif scope is None:
            self.scope = ()
        else:
            raise TypeError(f"Invalid scope: {scope}. ")
        self.state = state
        self.flow = "token" if app_is_client_only else "code"
        self.app_is_client_only = app_is_client_only

    @property
    def url(self) -> str:
        """Returns the URL you redirect the user to.

        You can use this property to get a URL that when opened on the user's
        device, shows Genius's authorization page where user clicks *Agree*
        to give your app access, and then Genius redirects user back to your
        redirect URI.
        """
        payload = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.flow,
        }
        if self.scope:
            payload["scope"] = " ".join(self.scope)
        if self.state:
            payload["state"] = self.state
        return OAuth2.auth_url + "?" + urlencode(payload)

    def get_user_token(
        self,
        code: str | None = None,
        url: str | None = None,
        state: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Gets a user token using the url or the code parameter..

        If you supply value for :obj:`code`, this method will use the value of the
        :obj:`code` parameter to request a token from Genius.

        If you use the :method`client_only_app` and supply the redirected URL,
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
        if state is not None and self.state != state:
            raise InvalidStateError("States do not match.")

        if code is not None:
            payload: dict[str, Any] = {
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
                "response_type": "code",
            }
            url = OAuth2.token_url.replace("https://api.genius.com/", "")
            res = self._make_request(url, "POST", data=payload, **kwargs)
            token = res["access_token"]
        elif url is not None:
            token = parse_redirected_url(url, self.flow)
        else:
            raise ValueError("You must pass either `code` or a non-None `url`.")
        return token

    def prompt_user(self) -> str:
        """Prompts current user for authentication.

        Opens a web browser for you to log in with Genius.
        Prompts to paste the URL after logging in to parse the
        *token* URL parameter.

        returns:
            :obj:`str`: User token.

        """
        url = self.url
        print("Opening browser for Genius login...")
        webbrowser.open(url)
        redirected = input("Please paste redirect URL: ").strip()

        if self.flow == "token":
            token = parse_redirected_url(redirected, self.flow)
        else:
            code = parse_redirected_url(redirected, self.flow)
            token = self.get_user_token(code)

        return token

    @classmethod
    def client_only_app(
        cls: type[Self],
        client_id: str,
        redirect_uri: str,
        scope: ScopeT | None = None,
        state: str | None = None,
    ) -> Self:
        """Returns an OAuth2 instance for a client-only app.

        Args:
            client_id (:obj:`str`): Client ID.
            redirect_uri (:obj:`str`): Whitelisted redirect URI.
            scope (:obj:`tuple` | :obj:`"all"`, optional): Token privilages.
            state (:obj:`str`, optional): Request state.

        returns:
            :class:`OAuth2`

        """
        return cls(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
            app_is_client_only=True,
        )

    @classmethod
    def full_code_exchange(
        cls: type[Self],
        client_id: str,
        redirect_uri: str,
        client_secret: str,
        scope: ScopeT | None = None,
        state: str | None = None,
    ) -> Self:
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
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"flow={self.flow!r}, "
            f"scope={self.scope!r}, "
            f"state={self.state!r}, "
            f"app_is_client_only={self.app_is_client_only!r})"
        )
