"""
Copyright (c) 2018, 2020, 2021 John W. Miller
Originally part of LyricsGenius, licensed under the MIT License.

Copyright (C) 2022 dopebnan
This file is part of AGenius.py.
You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

from .base import BaseEntity


class Artist(BaseEntity):
    """An artist with songs"""

    def __init__(self, client, json_dict):
        # Artist constructor
        body = json_dict
        super().__init__(body["id"])
        self._body = body
        self._client = client
        self.songs = []

        self.api_path = body["api_path"]
        self.is_verified = body["is_verified"]
        self.name = body["name"]
        self.url = body["url"]

    def __len__(self):
        return len(self.songs)

    def song(self, song_name):
        """
        Gets the artist's song.

        :param song_name: str, name of the song

        :return: types.Song
        """
        for song in self.songs:
            if song.title == song_name:
                return song

        return None

    def to_text(self):
        data = ' '.join(song.lyrics for song in self.songs)
        return data

    def __str__(self):
        msg = f"{self.name}, {len(self.songs)} songs"
        return msg
