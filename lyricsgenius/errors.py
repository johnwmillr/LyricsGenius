class InvalidStateError(Exception):
    """Exception for non-matching states."""


class PublicAPIForbiddenError(Exception):
    """Exception for forbidden access to PublicAPI methods."""
