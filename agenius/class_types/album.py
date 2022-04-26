"""
Copyright (C) 2022 dopebnan
This file is part of AGenius.py.
You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

from .base import BaseEntity
from .artist import Artist
from .song import Song


class Album(BaseEntity):
    """An album from Genius."""

    def __init__(self, client, json_dict, tracks):
        body = json_dict
        super().__init__(body["id"])
        self.body = body
        self._client = client
        self.artist = Artist(client, body["artist"])
        self.tracks = tracks
        self.release_date = body["release_date_components"]

        self._type = body["_type"]
        self.api_path = body["api_path"]
        self.cover_art_url = body["cover_art_url"]
        self.full_title = body["full_title"]
        self.name = body["name"]
        self.url = body["url"]

    def to_text(self):
        data = ' '.join(track.song.lyrics for track in self.tracks)
        return data


class Track(BaseEntity):
    """An album track from Genius"""

    def __init__(self, client, json_dict, lyrics):
        body = json_dict
        super().__init__(body["song"]["id"])
        self._body = body
        self.song = Song(client, body["song"], lyrics)
        self.number = body["number"]

    def to_text(self):
        data = self.song.lyrics
        return data

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}(number, song)"
