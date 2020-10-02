class TokenRequiredError(Exception):
    """Exception for endpoints that require a token."""

    def __init__(self, public_api=False):
        if public_api is False:
            message = "This method requires an access token."
        else:
            message = (
                "Using this method with the developers API needs an access token."
                " Get an access token or"
                " use the public API by setting"
                " public_api=True in method parameters or Genius.public_api=True"
            )
        super().__init__(message)
