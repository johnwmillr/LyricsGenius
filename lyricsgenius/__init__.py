# GeniusAPI
# John W. Miller
# See LICENSE for details
"""A library that provides a Python interface to the Genius API"""

import sys
assert sys.version_info[0] == 3, "LyricsGenius requires Python 3."
from lyricsgenius.genius import Genius
from lyricsgenius.api import API, PublicAPI
from lyricsgenius.auth import OAuth2
from lyricsgenius.utils import auth_from_environment

__author__ = 'John W. Miller'
__url__ = 'https://github.com/johnwmillr/LyricsGenius'
__description__ = 'A Python wrapper around the Genius API'
__license__ = 'MIT'
__version__ = '3.0.1'
