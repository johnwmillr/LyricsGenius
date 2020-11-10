import os

import vcr

from lyricsgenius import Genius


# Import client access token from environment variable
access_token = os.environ.get("GENIUS_ACCESS_TOKEN", None)
assert access_token is not None, (
    "Must declare environment variable: GENIUS_ACCESS_TOKEN")

# Genius client
genius = Genius(access_token, sleep_time=1.0, timeout=15, retries=3)

cassettes_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fixtures/cassettes'
)

# VCR Configs
test_vcr = vcr.VCR(
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    serializer='yaml',
    cassette_library_dir=cassettes_path,
    filter_headers=['authorization']
)
