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
