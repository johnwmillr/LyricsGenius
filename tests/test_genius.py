import os
import unittest
import lyricsgenius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist

# Import client access token from environment variable
client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
assert client_access_token is not None, "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
api = lyricsgenius.Genius(client_access_token)

class TestArtist(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		print("\n---------------------\nSetting up Artist tests...\n")
		cls.artist_name = "The Beatles"
		cls.new_song = "We can work it out"
		cls.max_songs = 3
		cls.artist = api.search_artist(cls.artist_name, max_songs=cls.max_songs)

	def test_artist(self):
		msg = "The returned object is not an instance of the Artist class."
		self.assertIsInstance(self.artist, Artist, msg)

	def test_name(self):
		msg = "The artist object name does not match the requested artist name."
		self.assertEqual(self.artist.name, self.artist_name, msg)

	def test_add_song_from_same_artist(self):
		msg = "The new song was not added to the artist object."
		self.artist.add_song(api.search_song(self.new_song,self.artist_name))
		self.assertEqual(self.artist.num_songs, self.max_songs+1, msg)

	def test_add_song_from_different_artist(self):
		msg = "A song from a different artist was incorrectly allowed to be added."
		self.artist.add_song(api.search_song("These Days","Jackson Browne"))
		self.assertEqual(self.artist.num_songs, self.max_songs, msg)


class TestSong(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		print("\n---------------------\nSetting up Song tests...\n")
		cls.artist_name = 'Andy Shauf'
		cls.song_title = 'Begin Again'
		cls.album = 'The Party'
		cls.year = '2016-05-20'
		cls.song = api.search_song(cls.song_title,cls.artist_name)

	def test_song(self):
		msg = "The returned object is not an instance of the Song class."
		self.assertIsInstance(self.song, Song, msg)

	def test_title(self):
		msg = "The returned song title does not match the title of the requested song."
		self.assertEqual(self.song.title, self.song_title, msg)

	def test_artist(self):
		msg = "The returned artist name does not match the artist of the requested song."
		self.assertEqual(self.song.artist, self.artist_name)

	def test_album(self):
		msg = "The returned album name does not match the album of the requested song."
		self.assertEqual(self.song.album, self.album, msg)

	def test_year(self):
		msg = "The returned year does not match the year of the requested song"
		self.assertEqual(self.song.year, self.year, msg)

	def test_lyrics(self):
		lyrics = 'Begin again\nThis time you should take a bow at the'
		self.assertTrue(self.song.lyrics.startswith(lyrics))

	def test_media(self):
		msg = "The returned song does not have a media attribute."
		self.assertTrue(hasattr(self.song, 'media'), msg)

