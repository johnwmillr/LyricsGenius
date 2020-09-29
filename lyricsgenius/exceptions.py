class TokenRequiredError(Exception):
    """Exception for endpoints that require a token."""

    def __init__(self, message="This method requires an access token."):
        super().__init__(message)
