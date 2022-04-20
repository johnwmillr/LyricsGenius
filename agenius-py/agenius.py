"""
Copyright (c) 2018, 2020, 2021 John W. Miller
Originally part of LyricsGenius, licensed under the MIT License.


Copyright (C) 2022 dopebnan
This file is part of AGenius.py.

AGenius.py is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or any later version.

AGenius.py is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

import re
import unicodedata

from bs4 import BeautifulSoup

from api_calls import API
from class_types import Song


class Genius(API):
    default_ex_terms = [r"track\s?list", "album art(work)?", "liner notes", "booklet", "credits", "interview", "skit",
                        "instrumental", "setlist"]

    def __init__(self, access_token, verbose=True, retries=0):
        """
        User-level interface with the Genius.com API.

        :param access_token: str, API key provided by Genius
        :param verbose: bool, turn logs on/off
        :param retries: int, number of retries in case of timeouts
            default: 0, requests are only made once
        :returns: Genius
        """
        # Genius client constructor
        super().__init__(
            access_token=access_token,
            retries=retries
        )

        self.verbose = verbose
        self.excluded_terms = self.default_ex_terms

    def is_lyrics(self, song):
        """
        Checks if result is actually a lyrics.

        :param song: str, title of the song
        :return: bool
        """
        if song["lyrics_state"] != "complete" or song.get("instrumental"):
            return False
        for term in self.excluded_terms:
            if term in unicodedata.normalize("NFKD", song["title"]):
                return False
        return True

    def item_from_search(self, response, search_term, type_, result_type):
        """
        Gets desired item from search results.

        This method tries to match the hits of the response to the response_term, and if it finds no match,
        returns the first appropriate hit (if there are any).

        :param response: dict, a response from Genius.search_all
        :param search_term: str, the search term to match with the hit
        :param type_: str, type of hit
        :param result_type: str, part of hit we want
        :return: str | None,
            None if there's not hit in response;
            Matched result if matching succeeds;
            First hit if matching fails;
        """

        # Convert to dictionary
        top_hits = response["hits"]

        hits = [hit for hit in top_hits if hit["type"] == type_]

        for hit in hits:
            item = hit["result"]
            if unicodedata.normalize(
                    "NFKD", item[result_type]).lower() == unicodedata.normalize("NFKD", search_term).lower():
                return item

        # Return first result that has lyrics
        for hit in hits:
            song = hit["result"]
            if self.is_lyrics(song):
                return song

        return hits[0]["result"] if hits else None

    def is_match(self, result, title, artist=None):
        """
        :param result: dict, result that needs to be checked
        :param title: str, title
        :param artist: str, artist
            default: None
        :return: bool, True if is a match
        """

        result_title = unicodedata.normalize("NFKD", result["title"])
        title_is_match = result_title == unicodedata.normalize("NFKD", title)
        if not artist:
            return title_is_match
        result_artist = unicodedata.normalize("NFKD", result["primary_artist"]["name"])
        return title_is_match and result_artist == unicodedata.normalize("NFKD", artist)

    async def lyrics(self, song_url):
        """
        Uses BeautifulSoup to scrape song info off of a Genius song URL

        You must supply either `song_id` or song_url`.

        :param song_url: str, song URL
        :returns: bool
        """

        # Scrape the song lyrics from the HTML
        response = await self._make_request_web(song_url)
        html = BeautifulSoup(
            response.replace('<br/>', '\n'),
            "html.parser"
        )

        # Determine the class of the div
        div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
        if div is None:
            if self.verbose:
                print("Couldn't find the lyrics section. "
                      "Please report this if the song has lyrics.\n"
                      f"Song URL: {song_url}")
            return None

        lyrics = div.get_text()
        return lyrics.strip("\n")

    async def search_song(self, title=None, artist="", song_id=None):
        """
        Searches for a specific song.

        You must pass either the title or song id.

        :param title: str, title of the song
        :param artist: str, name of the artist
            default: None
        :param song_id: int, song ID,
            default: None
        :return: class_types.Song | None,
            class_types.Song if successful;
            else None.
        """
        if title is None and song_id is None:
            assert any([title, song_id]), "You must pass either `title` or `song_id`"

        if self.verbose and title:
            if artist:
                print(f"Searching for '{title}' by '{artist}'..")
            else:
                print(f"Searching for '{title}'..")

        if song_id:
            result = await self.song(song_id)
            result = result["song"]
        else:
            search_term = f"{title} {artist}".strip()
            search_response = await self.search(search_term, 10)
            result = self.item_from_search(search_response, title, type_="song", result_type="title")

        # Exit search if no results
        if result is None:
            if self.verbose and title:
                print("No results found.")
            return False

        if not self.is_lyrics(result):
            if self.verbose:
                print("Song doesn't have lyrics.")
            return None

        song_id = result["id"]

        # Get info
        song_info = result
        lyrics = await self.lyrics(song_url=song_info["url"])

        if not lyrics:
            if self.verbose:
                print("No lyrics found")
            return None

        song = Song(self, song_info, lyrics)
        if self.verbose:
            print("Done.")
        return song
