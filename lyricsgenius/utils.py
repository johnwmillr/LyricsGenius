"""utility functions"""

import re
import os
from datetime import datetime
from urllib.parse import parse_qs, urlparse


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
        components = f
        year = str(components['year']) if components.get('year') else None
        month = str(components['month']).zfill(2) if components.get('month') else None
        day = str(components['day']).zfill(2) if components.get('day') else None
        if year and month:
            date = '{year}-{month}'.format(year=year, month=month)
            if day:
                date += '-' + day
        elif year:
            date = int(year)
        else:
            date = '0000-00-00'
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
