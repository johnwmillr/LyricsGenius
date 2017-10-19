import unittest
import genius
from genius.song import Song
from genius.artist import Artist
api = genius.Genius()

class TestArtist(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.artist = api.search_artist('Andy Shauf',max_songs=3)

	def test_artist(self):
		self.assertIsInstance(self.artist, Artist)

	def test_name(self):
		self.assertEqual(self.artist.name, 'Andy Shauf')

	def test_num_songs(self):
		self.assertEqual(self.artist.num_songs, 3)

	# TODO: add tests for add_song() and get_song()


class TestSong(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.song = api.search_song('Begin Again','Andy Shauf')

	def test_song(self):
		self.assertIsInstance(self.song, Song)

	def test_title(self):
		self.assertEqual(self.song.title, 'Begin Again')

	def test_artist(self):
		self.assertEqual(self.song.artist, 'Andy Shauf')

	def test_album(self):
		self.assertEqual(self.song.album, 'The Party')

	def test_year(self):
		self.assertEqual(self.song.year, '2016-05-20')

	def test_lyrics(self):
		lyrics = 'Begin again\nThis time you should take a bow at the'
		self.assertTrue(self.song.lyrics.startswith(lyrics))

	def test_media(self):
		self.assertTrue(isinstance(self.song.media,dict))




