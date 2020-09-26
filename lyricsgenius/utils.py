"""utility functions"""

import sys


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


def print_unicode(s):
    """Prints string that might have Unicode characters.

    Encodes string to ``utf-8`` and then decodes it based
    on the user's STDOUT's encoding, replacing erros in the process
    and then prints the string.

    Args:
        s (:obj:`str`): file name to sanitize.

    """
    print(s.encode('utf-8').decode(sys.stdout.encoding, errors='replace'))
