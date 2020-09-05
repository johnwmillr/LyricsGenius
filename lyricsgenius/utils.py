from urllib.parse import urlparse, parse_qs

"""Utility functions."""



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


def parse_redirected_url(url, flow):
    """
    Parse a URL for parameter 'code'/'token'.

    Args:
        url (:obj:`str`): The redirect URL.
        flow (:obj:`str`): authorization flow ('code' or 'token')

    Returns:
        :obj:`str`: value of 'code'/'token'.

    Raises:
        KeyError: if 'code'/'token' is not available or has multiple values.
    """
    query = urlparse(url).query
    code = parse_qs(query).get(flow, None)

    if code is None:
        raise KeyError("Parameter {} not available!".format(flow))
    elif len(code) > 1:
        raise KeyError("Multiple values for {}!".format(flow))

    return code[0]
