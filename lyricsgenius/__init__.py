# GeniusAPI
# John W. R. Miller
# See LICENSE for details
"""A library that provides a Python interface to the Genius API"""

import logging
import sys

assert sys.version_info[0] == 3, "LyricsGenius requires Python 3."
from lyricsgenius.api import API, PublicAPI
from lyricsgenius.auth import OAuth2
from lyricsgenius.genius import Genius
from lyricsgenius.utils import auth_from_environment

# Standard library best practice for packages: add NullHandler so that log
# records are silently discarded unless the *application* configures logging.
logging.getLogger("lyricsgenius").addHandler(logging.NullHandler())

_LOG_FORMAT = "%(levelname)s %(name)s: %(message)s"


def enable_logging(level: int = logging.DEBUG, fmt: str = _LOG_FORMAT) -> None:
    """Enable lyricsgenius logging output to stderr.

    A convenience wrapper around :func:`logging.basicConfig` that applies a
    sensible default format. Call this once near the top of your script before
    creating a :class:`Genius` instance.

    Args:
        level: Logging level (default ``logging.DEBUG``). Use
            ``logging.INFO`` to suppress debug-level messages.
        fmt: Log format string (default ``"%(levelname)s %(name)s: %(message)s"``).

    Example::

        import lyricsgenius
        lyricsgenius.enable_logging()
        lyricsgenius.enable_logging(logging.INFO)
        lyricsgenius.enable_logging(fmt="%(asctime)s %(levelname)s: %(message)s")
    """
    logging.basicConfig(level=level, format=fmt)
