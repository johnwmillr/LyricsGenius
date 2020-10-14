import unittest
import os

try:
    from .test_genius import genius
except ModuleNotFoundError:
    from test_genius import genius
from lyricsgenius.types import Song


class TestSong(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Song tests...\n")
        cls.artist_name = 'Andy Shauf'
        cls.song_title = 'begin again'  # Lowercase is intentional
        cls.album = 'The Party'
        cls.year = '2016-05-20'
        cls.song = genius.search_song(cls.song_title, cls.artist_name)
        genius.remove_section_headers = True
        cls.song_trimmed = genius.search_song(cls.song_title, cls.artist_name)

    def test_song(self):
        msg = "The returned object is not an instance of the Song class."
        self.assertIsInstance(self.song, Song, msg)

    def test_title(self):
        msg = "The returned song title does not match the title of the requested song."
        self.assertEqual(genius._clean_str(self.song.title),
                         genius._clean_str(self.song_title), msg)

    def test_artist(self):
        # The returned artist name does not match the artist of the requested song.
        self.assertEqual(self.song.artist, self.artist_name)

    # def test_album(self):
    #    msg = "The returned album name does not match the album of the requested song."
    #    self.assertEqual(self.song.album, self.album, msg)

    # def test_year(self):
    #    msg = "The returned year does not match the year of the requested song"
    #    self.assertEqual(self.song.year, self.year, msg)

    def test_lyrics_raw(self):
        lyrics = '[Verse 1: Andy Shauf]'
        self.assertTrue(self.song.lyrics.startswith(lyrics))

    def test_lyrics_no_section_headers(self):
        lyrics = 'Begin again\nThis time you should take a bow at the'
        self.assertTrue(self.song_trimmed.lyrics.startswith(lyrics))

    # def test_media(self):
    #    msg = "The returned song does not have a media attribute."
    #    self.assertTrue(hasattr(self.song, 'media'), msg)

    def test_result_is_lyrics(self):
        msg = "Did not reject a false-song."
        self.assertFalse(genius._result_is_lyrics('Beatles Tracklist'), msg)

    # def test_producer_artists(self):
    #    # Producer artist should be 'Andy Shauf'.
    #    self.assertEqual(self.song.producer_artists[0]["name"], "Andy Shauf")

    def test_saving_json_file(self):
        print('\n')
        extension = 'json'
        msg = "Could not save {} file.".format(extension)
        expected_filename = 'lyrics_save_test_file.' + extension
        filename = expected_filename.split('.')[0]

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving json file
        self.song.save_lyrics(filename=filename, extension=extension, overwrite=True)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting json file (now that file is written)
        try:
            self.song.save_lyrics(
                filename=expected_filename, extension=extension, overwrite=True)
            os.remove(expected_filename)
        except Exception:
            self.fail("Failed {} overwrite test".format(extension))
            os.remove(expected_filename)

    def test_saving_txt_file(self):
        print('\n')
        extension = 'txt'
        msg = "Could not save {} file.".format(extension)
        expected_filename = 'lyrics_save_test_file.' + extension
        filename = expected_filename.split('.')[0]

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving txt file
        self.song.save_lyrics(filename=filename,
                              extension=extension,
                              overwrite=True)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting txt file (now that file is written)
        try:
            self.song.save_lyrics(filename=filename,
                                  extension=extension,
                                  overwrite=True)
        except Exception:
            self.fail("Failed {} overwrite test".format(extension))
        os.remove(expected_filename)
