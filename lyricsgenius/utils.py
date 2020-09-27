"""utility functions"""

from datetime import datetime


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


def _convert_to_datetime(f):
    if f is None:
        return None

    if '-' in f:
        date_format = "%Y-%m-%d"
    elif ',' in f:
        date_format = "%B %d, %Y"
    elif f.isdigit():
        date_format = "%Y"
    else:
        date_format = "%B %Y"

    return datetime.strptime(f, date_format)
