import unittest

from . import genius


class TestEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Endpoint tests...\n")

        cls.search_term = "Ezra Furman"
        cls.song_title_only = "99 Problems"
        cls.tag = genius.tag('pop')

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

    def test_tag_results(self):
        r = self.tag

        self.assertEqual(r['next_page'], 2)
        self.assertEqual(len(r['hits']), 20)

    def test_tag_first_result(self):
        artists = ['Luis Fonsi', 'Daddy Yankee']
        featured_artists = ['Justin Bieber']
        song_title = "Despacito (Remix)"
        title_with_artists = (
            "Despacito (Remix) by Luis Fonsi & Daddy Yankee (Ft. Justin Bieber)"
        )
        url = "https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics"

        first_song = self.tag['hits'][0]

        self.assertEqual(artists, first_song['artists'])
        self.assertEqual(featured_artists, first_song['featured_artists'])
        self.assertEqual(song_title, first_song['title'])
        self.assertEqual(title_with_artists, first_song['title_with_artists'])
        self.assertEqual(url, first_song['url'])


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
        lyrics = genius.lyrics(song_url=self.song_url)
        self.assertTrue(lyrics.endswith(self.lyrics_ending))

    def test_lyrics_with_id(self):
        lyrics = genius.lyrics(self.song_id)
        self.assertTrue(lyrics.endswith(self.lyrics_ending))
