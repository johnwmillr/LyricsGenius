"""utility functions"""
import functools
import re
import os
import sys
import unicodedata
from datetime import datetime
from string import punctuation
from urllib.parse import parse_qs, urlparse

from .errors import PublicAPIForbiddenError


def auth_from_environment():
    """Gets credentials from environment variables.

    Uses the following env vars: ``GENIUS_CLIENT_ID``,
    ``GENIUS_REDIRECT_URI`` and ``GENIUS_CLIENT_SECRET``.

    Returns:
        :obj:`tuple`: client ID, redirect URI and client secret.
        Replaces variables that are not present with :obj:`None`.

    """
    client_id = os.environ.get('GENIUS_CLIENT_ID')
    redirect_uri = os.environ.get('GENIUS_REDIRECT_URI')
    client_secret = os.environ.get('GENIUS_CLIENT_SECRET')
    return client_id, redirect_uri, client_secret


def uses_public_api(func):
    """Allows execution of func only if allow_public_api=True

    Raises:
        PublicAPIForbiddenError: If allow_public_api=False

    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.allow_public_api:
            raise PublicAPIForbiddenError(
                ("{} uses Public API methods, but genius.allow_public_api=False."
                 "\nFor more info visit "
                 "https://lyricsgenius.rtfd.io/en/stable/how_it_works.html"
                 ).format(type(self).__name__ + "." + func.__name__)
            )
        return func(self, *args, **kwargs)
    return wrapper


def convert_to_datetime(f):
    """Converts argument to a datetime object.

    Args:
        f (:obj:`str`| :obj:`dict`): string or dictionary containing
            date components.

    Returns:
        :class:`datetime`: datetime object.
    """
    if f is None:
        return None

    if isinstance(f, dict):
        year = f.get('year')
        month = f.get('month')
        day = f.get('day')
        if year and month:
            date = '{year}-{month:02}'.format(year=year, month=month)
            if day:
                date += '-{day:02}'.format(day=day)
        elif year:
            date = str(year)
        else:
            return None
        f = date

    if f.count('-') == 2:
        date_format = "%Y-%m-%d"
    elif f.count('-') == 1:
        date_format = "%Y-%m"
    elif ',' in f:
        date_format = "%B %d, %Y"
    elif f.isdigit():
        date_format = "%Y"
    else:
        date_format = "%B %Y"

    return datetime.strptime(f, date_format)


def clean_str(s):
    """Cleans a string to help with string comparison.

    Removes punctuation and returns
    a stripped, NFKC normalized string in lowercase.

    Args:
        s (:obj:`str`): A string.

    Returns:
        :obj:`str`: Cleaned string.

    """
    punctuation_ = punctuation + "’" + "\u200b"
    string = s.translate(str.maketrans('', '', punctuation_)).strip().lower()
    return unicodedata.normalize("NFKC", string)


def parse_redirected_url(url, flow):
    """Parse a URL for parameter 'code'/'token'.

    Args:
        url (:obj:`str`): The redirect URL.
        flow (:obj:`str`): authorization flow ('code' or 'token')

    Returns:
        :obj:`str`: value of 'code'/'token'.

    Raises:
        KeyError: if 'code'/'token' is not available or has multiple values.

    """
    if flow == 'code':
        query = urlparse(url).query
    elif flow == 'token':
        query = re.sub(r'.*#access_', '', url)
    parameters = parse_qs(query)
    code = parameters.get(flow, None)

    if code is None:
        raise KeyError("Parameter {} not available!".format(flow))
    elif len(code) > 1:
        raise KeyError("Multiple values for {}!".format(flow))

    return code[0]


def safe_unicode(s):
    """Encodes and decodes string based on user's STDOUT.

    Encodes string to ``utf-8`` and then decodes it based
    on the user's STDOUT's encoding, replacing erros in the process.

    Args:
        s (:obj:`str`): a string.

    Returns:
        :obj:`str`

    """
    return s.encode('utf-8').decode(sys.stdout.encoding, errors='replace')


def sanitize_filename(f):
    """Removes invalid characters from file name.

    Args:
        f (:obj:`str`): file name to sanitize.

    Returns:
        :obj:`str`: sanitized file name including only alphanumeric
        characters, spaces, dots or underlines.

    """
    keepchars = (" ", ".", "_")
    return "".join(c for c in f if c.isalnum() or c in keepchars).rstrip()
