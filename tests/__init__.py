import os
import warnings

from lyricsgenius import Genius


def get_genius_client() -> Genius:
    """Factory function to create Genius client instances for tests."""
    if (access_token := os.environ.get("GENIUS_ACCESS_TOKEN")) is None:
        raise KeyError(
            "No GENIUS_ACCESS_TOKEN found in environment variables. "
            "Cannot run tests that require API interaction."
        )

    return Genius(access_token, sleep_time=1.0, timeout=15, retries=3)
