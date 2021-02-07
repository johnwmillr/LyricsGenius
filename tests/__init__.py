import os

from lyricsgenius import Genius


# Import client access token from environment variable
access_token = os.environ.get("GENIUS_ACCESS_TOKEN", None)
assert access_token is not None, (
    "Must declare environment variable: GENIUS_ACCESS_TOKEN")

# Genius client
genius = Genius(access_token, sleep_time=1.0, timeout=15, retries=3)
