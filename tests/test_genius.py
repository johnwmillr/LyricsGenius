import os
import unittest
from lyricsgenius import Genius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist
from lyricsgenius.utils import sanitize_filename


# Import client access token from environment variable
client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
assert client_access_token is not None, (
    "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN")
genius = Genius(client_access_token, sleep_time=1.0, timeout=15)


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

    def test_referents_web_page(self):
        msg = "Returned referent API path is different than expected."
        id_ = 10347
        r = genius.referents(web_page_id=id_)
        real = r['referents'][0]['api_path']
        expected = '/referents/11828416'
        self.assertTrue(real == expected, msg)

    def test_referents_invalid_input(self):
        # Method should prevent inputs for both song and web_pag ID.
        with self.assertRaises(AssertionError):
            genius.referents(song_id=1, web_page_id=1)

    def test_referents_no_inputs(self):
        # Must supply `song_id`, `web_page_id`, or `created_by_id`.
        with self.assertRaises(AssertionError):
            genius.referents()

    def test_annotation(self):
        msg = "Returned annotation API path is different than expected."
        id_ = 10225840
        r = genius.annotation(id_)
        real = r['annotation']['api_path']
        expected = '/annotations/10225840'
        self.assertEqual(real, expected, msg)

    def test_song_annotations(self):
        msg = "Incorrect song annotation response."
        r = sorted(genius.song_annotations(1))
        real = r[0][0]
        expected = "And I’ma keep ya fresh"
        self.assertEqual(real, expected, msg)


class TestAlbumMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up album methods tests...\n")
        cls.search_term = "Ezra Furman"
        cls.song_title_only = "99 Problems"

    def test_album(self):
        album_id = 104614
        msg = "Album ID did not match."
        r = genius.album(album_id)
        self.assertTrue(r['id'] == album_id, msg)

    def test_albums_charts(self):
        album_id = 104614
        msg = "Album ID did not match."
        r = genius.album(album_id)
        self.assertTrue(r['id'] == album_id, msg)


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

    def test_add_song_from_different_artist(self):
        msg = "A song from a different artist was incorrectly allowed to be added."
        self.artist.add_song(genius.search_song("These Days", "Jackson Browne"))
        self.assertEqual(self.artist.num_songs, self.max_songs, msg)

    def test_artist_with_includes_features(self):
        # The artist did not get songs returned that they were featured in.
        name = "Swae Lee"
        result = (genius
                  .search_artist(
                      name,
                      max_songs=1,
                      include_features=True)
                  .songs[0]
                  ._body['primary_artist']['name'])
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

    def test_producer_artists(self):
        # Producer artist should be 'Andy Shauf'.
        self.assertEqual(self.song.producer_artists[0]["name"], "Andy Shauf")

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
