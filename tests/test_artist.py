import unittest
import os

from . import genius
from lyricsgenius.types import Artist
from lyricsgenius.utils import sanitize_filename


class TestArtist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Artist tests...\n")

        cls.artist_name = "The Beatles"
        cls.new_song = "Paperback Writer"
        cls.max_songs = 2
        cls.artist = genius.search_artist(
            cls.artist_name, max_songs=cls.max_songs)

    def test_artist(self):
        msg = "The returned object is not an instance of the Artist class."
        self.assertIsInstance(self.artist, Artist, msg)

    def test_correct_artist_name(self):
        msg = "Returned artist name does not match searched artist."
        name = "Queen"
        result = genius.search_artist(name, max_songs=1).name
        self.assertEqual(name, result, msg)

    def test_zero_songs(self):
        msg = "Songs were downloaded even though 0 songs was requested."
        name = "Queen"
        result = genius.search_artist(name, max_songs=0).songs
        self.assertEqual(0, len(result), msg)

    def test_name(self):
        msg = "The artist object name does not match the requested artist name."
        self.assertEqual(self.artist.name, self.artist_name, msg)

    def test_add_song_from_same_artist(self):
        msg = "The new song was not added to the artist object."
        self.artist.add_song(genius.search_song(self.new_song, self.artist_name))
        self.assertEqual(self.artist.num_songs, self.max_songs + 1, msg)

    def test_song(self):
        msg = "Song was not in artist's songs."
        song = self.artist.song(self.new_song)
        self.assertIsNotNone(song, msg)

    def test_add_song_from_different_artist(self):
        msg = "A song from a different artist was incorrectly allowed to be added."
        self.artist.add_song(genius.search_song("These Days", "Jackson Browne"))
        self.assertEqual(self.artist.num_songs, self.max_songs, msg)

    def test_artist_with_includes_features(self):
        # The artist did not get songs returned that they were featured in.
        name = "Swae Lee"
        result = genius.search_artist(
            name,
            max_songs=1,
            include_features=True)
        result = result.songs[0].artist
        self.assertNotEqual(result, name)

    def determine_filenames(self, extension):
        expected_filenames = []
        for song in self.artist.songs:
            fn = "lyrics_{name}_{song}.{ext}".format(name=self.artist.name,
                                                     song=song.title,
                                                     ext=extension)
            fn = sanitize_filename(fn.lower().replace(" ", ""))
            expected_filenames.append(fn)
        return expected_filenames

    def test_saving_json_file(self):
        print('\n')
        extension = 'json'
        msg = "Could not save {} file.".format(extension)
        expected_filename = ('Lyrics_'
                             + self.artist.name.replace(' ', '')
                             + '.'
                             + extension)

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving json file
        self.artist.save_lyrics(extension=extension, overwrite=True)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting json file (now that file is written)
        try:
            self.artist.save_lyrics(extension=extension, overwrite=True)
        except Exception:
            self.fail("Failed {} overwrite test".format(extension))
        os.remove(expected_filename)

    def test_saving_txt_file(self):
        print('\n')
        extension = 'txt'
        msg = "Could not save {} file.".format(extension)
        expected_filename = ('Lyrics_'
                             + self.artist.name.replace(' ', '')
                             + '.'
                             + extension)

        # Remove the test file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        # Test saving txt file
        self.artist.save_lyrics(extension=extension, overwrite=True)
        self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting txt file (now that file is written)
        try:
            self.artist.save_lyrics(
                extension=extension, overwrite=True)
        except Exception:
            self.fail("Failed {} overwrite test".format(extension))
        os.remove(expected_filename)
