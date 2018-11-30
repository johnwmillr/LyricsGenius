import os
import unittest
import lyricsgenius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist

# Import client access token from environment variable
client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
assert client_access_token is not None, "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
api = lyricsgenius.Genius(client_access_token, sleep_time=0.5)


class TestEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Endpoint tests...\n")
        cls.search_term = "Ezra Furman"

    def test_search_genius_web(self):
        # TODO: test more than just a 200 response
        msg = "Response was None."
        r = api.search_genius_web(self.search_term)
        self.assertTrue(r is not None, msg)


class TestArtist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Artist tests...\n")
        cls.artist_name = "The Beatles"
        cls.new_song = "Paperback Writer"
        cls.max_songs = 2
        cls.artist = api.search_artist(
            cls.artist_name, max_songs=cls.max_songs)

    def test_artist(self):
        msg = "The returned object is not an instance of the Artist class."
        self.assertIsInstance(self.artist, Artist, msg)

    def test_name(self):
        msg = "The artist object name does not match the requested artist name."
        self.assertEqual(self.artist.name, self.artist_name, msg)

    def test_add_song_from_same_artist(self):
        msg = "The new song was not added to the artist object."
        self.artist.add_song(api.search_song(self.new_song, self.artist_name))
        self.assertEqual(self.artist.num_songs, self.max_songs+1, msg)

    def test_add_song_from_different_artist(self):
        msg = "A song from a different artist was incorrectly allowed to be added."
        self.artist.add_song(api.search_song("These Days", "Jackson Browne"))
        self.assertEqual(self.artist.num_songs, self.max_songs, msg)

    def test_saving_json_file(self):
        print('\n')
        format_ = 'json'
        msg = "Could not save {} file.".format(format_)
        expected_filename = 'tests/lyrics_save_test_file.' + format_
        filename = expected_filename.split('.')[0]

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving json file
        self.artist.save_lyrics(filename=filename, format_=format_)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting json file
        try:
            self.artist.save_lyrics(
                filename=filename, format_=format_, overwrite=True)
            os.remove(expected_filename)
        except:
            self.fail("Failed {} overwrite test".format(format_))
            os.remove(expected_filename)

    def test_saving_txt_file(self):
        print('\n')
        format_ = 'txt'
        msg = "Could not save {} file.".format(format_)
        expected_filename = 'tests/lyrics_save_test_file.' + format_
        filename = expected_filename.split('.')[0]

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving txt file
        self.artist.save_lyrics(filename=filename, format_=format_)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting txt file
        try:
            self.artist.save_lyrics(
                filename=filename, format_=format_, overwrite=True)
            os.remove(expected_filename)
        except:
            self.fail("Failed {} overwrite test".format(format_))
            os.remove(expected_filename)


class TestSong(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Song tests...\n")
        cls.artist_name = 'Andy Shauf'
        cls.song_title = 'begin again'  # Lowercase is intentional
        cls.album = 'The Party'
        cls.year = '2016-05-20'
        cls.song = api.search_song(cls.song_title, cls.artist_name)
        api.remove_section_headers = True
        cls.song_trimmed = api.search_song(cls.song_title, cls.artist_name)

    def test_song(self):
        msg = "The returned object is not an instance of the Song class."
        self.assertIsInstance(self.song, Song, msg)

    def test_title(self):
        msg = "The returned song title does not match the title of the requested song."
        self.assertEqual(api._clean_str(self.song.title),
                         api._clean_str(self.song_title), msg)

    def test_artist(self):
        msg = "The returned artist name does not match the artist of the requested song."
        self.assertEqual(self.song.artist, self.artist_name)

    def test_album(self):
        msg = "The returned album name does not match the album of the requested song."
        self.assertEqual(self.song.album, self.album, msg)

    def test_year(self):
        msg = "The returned year does not match the year of the requested song"
        self.assertEqual(self.song.year, self.year, msg)

    def test_lyrics_raw(self):
        lyrics = '[Verse 1: Andy Shauf]'
        self.assertTrue(self.song.lyrics.startswith(lyrics))

    def test_lyrics_no_section_headers(self):
        lyrics = 'Begin again\nThis time you should take a bow at the'
        self.assertTrue(self.song_trimmed.lyrics.startswith(lyrics))

    def test_media(self):
        msg = "The returned song does not have a media attribute."
        self.assertTrue(hasattr(self.song, 'media'), msg)

    def test_result_is_lyrics(self):
        msg = "Did not reject a false-song."
        self.assertFalse(api._result_is_lyrics('Beatles Tracklist'), msg)

    def test_saving_json_file(self):
        print('\n')
        format_ = 'json'
        msg = "Could not save {} file.".format(format_)
        expected_filename = 'tests/lyrics_save_test_file.' + format_
        filename = expected_filename.split('.')[0]

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving json file
        self.song.save_lyrics(filename=filename, format_=format_)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting json file
        try:
            self.song.save_lyrics(
                filename=filename, format_=format_, overwrite=True)
            os.remove(expected_filename)
        except:
            self.fail("Failed {} overwrite test".format(format_))
            os.remove(expected_filename)

    def test_saving_txt_file(self):
        print('\n')
        format_ = 'txt'
        msg = "Could not save {} file.".format(format_)
        expected_filename = 'tests/lyrics_save_test_file.' + format_
        filename = expected_filename.split('.')[0]

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving txt file
        self.song.save_lyrics(filename=filename, format_=format_)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting txt file
        try:
            self.song.save_lyrics(
                filename=filename, format_=format_, overwrite=True)
            os.remove(expected_filename)
        except:
            self.fail("Failed {} overwrite test".format(format_))
            os.remove(expected_filename)
