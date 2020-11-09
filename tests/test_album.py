import unittest
import os
import warnings

import vcr

from . import genius, test_vcr
from lyricsgenius.types import Album


class TestAlbum(unittest.TestCase):

    @classmethod
    @test_vcr.use_cassette(path_transformer=vcr.VCR.ensure_suffix(' album.yaml'),
                           serializer='yaml')
    def setUpClass(cls):
        print("\n---------------------\nSetting up Album tests...\n")
        warnings.simplefilter("ignore", ResourceWarning)
        cls.album_name = "The Party"
        cls.artist_name = "Andy Shauf"
        cls.num_songs = 10
        cls.album = genius.search_album(
            cls.album_name,
            cls.artist_name
        )

    def test_type(self):
        self.assertIsInstance(self.album, Album)

    def test_album_name(self):
        self.assertEqual(self.album.name, self.album_name)

    def test_album_artist(self):
        self.assertEqual(self.album.artist.name, self.artist_name)

    def test_songs(self):
        self.assertEqual(len(self.album.songs), self.num_songs)

    def test_saving_json_file(self):
        print('\n')
        extension = 'json'
        msg = "Could not save {} file.".format(extension)
        expected_filename = ('Lyrics_'
                             + self.album.name.replace(' ', '')
                             + '.'
                             + extension)

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving json file
        self.album.save_lyrics(extension=extension, overwrite=True)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting json file (now that file is written)
        try:
            self.album.save_lyrics(extension=extension, overwrite=True)
        except Exception:
            self.fail("Failed {} overwrite test".format(extension))
        os.remove(expected_filename)

    def test_saving_txt_file(self):
        print('\n')
        extension = 'txt'
        msg = "Could not save {} file.".format(extension)
        expected_filename = ('Lyrics_'
                             + self.album.name.replace(' ', '')
                             + '.'
                             + extension)

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving txt file
        self.album.save_lyrics(extension=extension, overwrite=True)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting txt file (now that file is written)
        try:
            self.album.save_lyrics(
                extension=extension, overwrite=True)
        except Exception:
            self.fail("Failed {} overwrite test".format(extension))
        os.remove(expected_filename)
