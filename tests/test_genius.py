import os
import unittest
from lyricsgenius.api import Genius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist

# Import client access token from environment variable
client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
assert client_access_token is not None, "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
genius = Genius(client_access_token, sleep_time=0.5)


class TestEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Endpoint tests...\n")
        cls.search_term = "Ezra Furman"
        cls.song_title_only = "99 Problems"

    def test_search_genius_web(self):
        # TODO: test more than just a 200 response
        msg = "Response was None."
        r = genius.search_genius_web(self.search_term)
        self.assertTrue(r is not None, msg)

    def test_search_song(self):
        # Empty response
        response = genius.search_song('')
        self.assertIsNone(response)

        # Exact match exact search
        response = genius.search_song(self.song_title_only)
        self.assertTrue(response.title.lower() == self.song_title_only.lower())

        #Spaced out search
        response = genius.search_song("  \t 99  \t \t\tProblems   ")
        self.assertTrue(response.title.lower() == self.song_title_only.lower())

        # No title match because of artist
        response = genius.search_song(self.song_title_only, artist="Drake")
        self.assertFalse(response.title.lower() == self.song_title_only.lower())


class TestArtist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Artist tests...\n")
        cls.artist_name = "The Beatles"
        cls.new_song = "Paperback Writer"
        cls.max_songs = 2
        cls.artist = genius.search_artist(
            cls.artist_name, max_songs=cls.max_songs)

    def sanitize_filename(f):
        keepchars = (" ", ".", "_")
        s = "".join(c for c in f if c.isalnum() or c in keepchars).rstrip()
        return s

    def test_artist(self):
        msg = "The returned object is not an instance of the Artist class."
        self.assertIsInstance(self.artist, Artist, msg)

    def test_name(self):
        msg = "The artist object name does not match the requested artist name."
        self.assertEqual(self.artist.name, self.artist_name, msg)

    def test_add_song_from_same_artist(self):
        msg = "The new song was not added to the artist object."
        self.artist.add_song(genius.search_song(self.new_song, self.artist_name))
        self.assertEqual(self.artist.num_songs, self.max_songs+1, msg)

    def test_add_song_from_different_artist(self):
        msg = "A song from a different artist was incorrectly allowed to be added."
        self.artist.add_song(genius.search_song("These Days", "Jackson Browne"))
        self.assertEqual(self.artist.num_songs, self.max_songs, msg)

    def determine_filenames(self, extension):
        expected_filenames = []
        for song in self.artist.songs:
            fn = "lyrics_{name}_{song}.{ext}".format(name=self.artist.name,
                                                     song=song.title,
                                                     ext=extension)
            fn = song.sanitize_filename(fn.lower().replace(" ", ""))
            expected_filenames.append(fn)
        return expected_filenames

    def test_saving_json_file(self):
        print('\n')
        extension = 'json'
        msg = "Could not save {} file.".format(extension)
        expected_filenames = self.determine_filenames(extension)

        # Remove the test file if it already exists
        for expected_filename in expected_filenames:
            if os.path.isfile(expected_filename):
                os.remove(expected_filename)

        # Test saving json file
        self.artist.save_lyrics(extension=extension, overwrite=True)
        for expected_filename in expected_filenames:
            self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting json file (now that file is written)
        try:
            self.artist.save_lyrics(extension=extension, overwrite=True)
        except:
            self.fail("Failed {} overwrite test".format(extension))
        for expected_filename in expected_filenames:
            os.remove(expected_filename)

    def test_saving_txt_file(self):
        print('\n')
        extension = 'txt'
        msg = "Could not save {} file.".format(extension)
        expected_filenames = self.determine_filenames(extension)

        # Remove the test file if it already exists
        for expected_filename in expected_filenames:
            if os.path.isfile(expected_filename):
                os.remove(expected_filename)

        # Test saving txt file
        self.artist.save_lyrics(extension=extension, overwrite=True)
        for expected_filename in expected_filenames:
            self.assertTrue(os.path.isfile(expected_filename), msg)

        # Test overwriting txt file (now that file is written)
        try:
            self.artist.save_lyrics(
                extension=extension, overwrite=True)
        except:
            self.fail("Failed {} overwrite test".format(extension))
        for expected_filename in expected_filenames:
            os.remove(expected_filename)


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
        self.assertFalse(genius._result_is_lyrics('Beatles Tracklist'), msg)

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
        except:
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
        except:
            self.fail("Failed {} overwrite test".format(extension))
        os.remove(expected_filename)

    # def test_bad_chars_in_filename(self):
    #     print("\n")
    #     extension = "json"
    #     msg = "Could not save {} file.".format(extension)
    #     song = genius.search_song("Blessed rainbow", "Ariana Grande")
    #     expected_filename = "lyrics_arianagrande_blessedrainbow.json"

    #     # Remove the test file if it already exists
    #     if os.path.isfile(expected_filename):
    #         os.remove(expected_filename)

    #     # Test saving txt file
    #     song.save_lyrics(extension=extension, overwrite=True)
    #     self.assertTrue(os.path.isfile(expected_filename), msg)
    #     os.remove(expected_filename)
