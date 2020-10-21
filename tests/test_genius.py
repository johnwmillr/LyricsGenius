import os
import unittest

from lyricsgenius import Genius


# Import client access token from environment variable
access_token = os.environ.get("GENIUS_ACCESS_TOKEN", None)
assert access_token is not None, (
    "Must declare environment variable: GENIUS_ACCESS_TOKEN")
genius = Genius(access_token, sleep_time=1.0, timeout=15)


class TestEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Endpoint tests...\n")
        cls.search_term = "Ezra Furman"
        cls.song_title_only = "99 Problems"

    def test_search_song(self):
        artist = "Jay-Z"
        # Empty response
        response = genius.search_song('')
        self.assertIsNone(response)

        # Pass no title and ID
        with self.assertRaises(AssertionError):
            genius.search_song()

        # Search by song ID
        response = genius.search_song(song_id=1)
        self.assertIsNotNone(response)

        # Exact match exact search
        response = genius.search_song(self.song_title_only)
        self.assertTrue(response.title.lower() == self.song_title_only.lower())

        # Song with artist name
        response = genius.search_song(self.song_title_only, artist)
        self.assertTrue(response.title.lower() == self.song_title_only.lower())

        # Spaced out search
        response = genius.search_song("  \t 99  \t \t\tProblems   ", artist)
        self.assertTrue(response.title.lower() == self.song_title_only.lower())

        # No title match because of artist
        response = genius.search_song(self.song_title_only, artist="Drake")
        self.assertFalse(response.title.lower() == self.song_title_only.lower())

    def test_song_annotations(self):
        msg = "Incorrect song annotation response."
        r = sorted(genius.song_annotations(1))
        real = r[0][0]
        expected = "(I’m at bat)"
        self.assertEqual(real, expected, msg)


class TestLyrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up lyrics tests...\n")
        cls.song_url = "https://genius.com/Andy-shauf-begin-again-lyrics"
        cls.song_id = 2885745
        cls.lyrics_ending = (
            "[Outro]"
            "\nNow I’m kicking leaves"
            "\nCursing the one that I love and the one I don’t"
            "\nI wonder who you’re thinking of"
        )

    def test_lyrics_with_url(self):
        lyrics = genius.lyrics(self.song_url)
        self.assertTrue(lyrics.endswith(self.lyrics_ending))

    def test_lyrics_with_id(self):
        lyrics = genius.lyrics(self.song_id)
        self.assertTrue(lyrics.endswith(self.lyrics_ending))
