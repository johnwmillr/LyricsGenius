import warnings
from typing import Any, cast

import pytest

from lyricsgenius.genius import Genius
from tests import get_genius_client

try:
    genius = get_genius_client()
except KeyError:
    warnings.warn(
        "Skipping API tests because no GENIUS_ACCESS_TOKEN was found in the environment variables.",
        stacklevel=1,
    )


@pytest.mark.skip(reason="API method tests still under development / require live API.")
class TestAPI:  # pragma: no cover - legacy style converted
    def test_account(self) -> None:
        r = genius.account()
        assert "user" in r, (
            "No user detail was returned. "
            "Are you sure you're using a user access token?"
        )

    def test_annotation(self) -> None:
        id_ = 10225840
        r = genius.annotation(id_)
        assert r["annotation"]["api_path"] == "/annotations/10225840", (
            "Returned annotation API path is different than expected."
        )

    def test_manage_annotation(self) -> None:
        example_text = "The annotation"
        new_annotation = genius.create_annotation(
            example_text, "https://example.com", "illustrative examples", title="test"
        )["annotation"]
        assert new_annotation["body"]["plain"] == example_text, (
            "Annotation text did not match the one that was passed."
        )

        try:
            example_text_two = "Updated annotation"
            r = genius.update_annotation(
                new_annotation["id"],
                example_text_two,
                "https://example.com",
                "illustrative examples",
                title="test",
            )["annotation"]
            assert r["body"]["plain"] == example_text_two, (
                "Updated annotation text did not match the one that was passed."
            )

            r = genius.upvote_annotation(11828417)
            assert r is not None, "Upvote was not registered."

            r = genius.downvote_annotation(11828417)
            assert r is not None, "Downvote was not registered."

            r = genius.unvote_annotation(11828417)
            assert r is not None, "Vote was not removed."
        finally:
            r = genius.delete_annotation(new_annotation["id"])
            assert r == 204, "Annotation was not deleted."

    def test_referents_web_page(self) -> None:
        id_ = 10347
        r = genius.referents(web_page_id=id_)
        assert r["referents"][0]["api_path"] == "/referents/11828416", (
            "Returned referent API path is different than expected."
        )

    def test_referents_no_inputs(self) -> None:
        # Must supply `song_id`, `web_page_id`, or `created_by_id`.
        with pytest.raises(AssertionError):
            genius.referents()

    def test_referents_invalid_input(self) -> None:
        # Method should prevent inputs for both song and web_pag ID.
        with pytest.raises(AssertionError):
            genius.referents(song_id=1, web_page_id=1)

    def test_web_page(self) -> None:
        url = "https://docs.genius.com"
        r = genius.web_page(raw_annotatable_url=url)
        assert r["web_page"]["api_path"] == "/web_pages/10347", (
            "Returned web page API path is different than expected."
        )


@pytest.mark.skip(reason="Endpoints tests still under development / require live API.")
class TestEndpoints:  # pragma: no cover - legacy style converted
    search_term: str = "Ezra Furman"
    song_title_only: str = "99 Problems"
    tag: Any = genius.tag("pop")

    def test_search_song(self) -> None:
        artist = "Jay-Z"
        response = genius.search_song("")
        assert response is None
        with pytest.raises(AssertionError):
            genius.search_song()
        response = genius.search_song(song_id=1)
        assert response is not None
        response = genius.search_song(self.song_title_only)
        if response is not None:
            assert response.title.lower() == self.song_title_only.lower()
        response = genius.search_song(self.song_title_only, artist)
        if response is not None:
            assert response.title.lower() == self.song_title_only.lower()
        response = genius.search_song("  \t 99  \t \t\tProblems   ", artist)
        assert (
            response is not None
            and response.title.lower() == self.song_title_only.lower()
        )
        response = genius.search_song(self.song_title_only, artist="Drake")
        if response is not None:
            assert response.title.lower() != self.song_title_only.lower()

    def test_song_annotations(self) -> None:
        r = sorted(genius.song_annotations(1))
        real = r[0][0]
        expected = "(I'm at bat)"
        assert real == expected

    def test_tag_results(self) -> None:
        r = self.tag
        if r is not None:
            r_dict = cast(dict[str, Any], r)
            assert r_dict["next_page"] == 2
            assert len(cast(list[Any], r_dict["hits"])) == 20

    def test_tag_first_result(self) -> None:
        artists = ["Luis Fonsi", "Daddy Yankee"]
        featured_artists = ["Justin Bieber"]
        song_title = "Despacito (Remix)"
        title_with_artists = (
            "Despacito (Remix) by Luis Fonsi & Daddy Yankee (Ft. Justin Bieber)"
        )
        url = "https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics"
        if self.tag is None:
            pytest.skip("Tag request returned None")
        first_song = cast(dict[str, Any], self.tag)["hits"][0]
        assert artists == first_song["artists"]
        assert featured_artists == first_song["featured_artists"]
        assert song_title == first_song["title"]
        assert title_with_artists == first_song["title_with_artists"]
        assert url == first_song["url"]


@pytest.mark.skip(
    reason="Lyrics scraping tests still under development / require live API."
)
class TestLyrics:  # pragma: no cover - legacy style converted
    song_url = "https://genius.com/Andy-shauf-begin-again-lyrics"
    song_id = 2885745
    lyrics_ending = (
        "[Outro]"
        "\nNow I'm kicking leaves"
        "\nCursing the one that I love and the one I don't"
        "\nI wonder who you're thinking of"
    )

    def test_lyrics_with_url(self) -> None:
        lyrics = genius.lyrics(song_url=self.song_url)
        if lyrics is None:
            raise AssertionError("Expected lyrics but got None")
        assert lyrics.endswith(self.lyrics_ending)

    def test_lyrics_with_id(self) -> None:
        lyrics = genius.lyrics(self.song_id)
        if lyrics is None:
            raise AssertionError("Expected lyrics but got None")
        assert lyrics.endswith(self.lyrics_ending)
