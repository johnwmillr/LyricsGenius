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


@pytest.fixture()
def _result_is_lyrics_genius() -> Genius:
    """Provide a Genius instance for _result_is_lyrics tests with verbosity off."""
    return Genius(verbose=False)


def _call(g: Genius, song: dict[str, Any]) -> bool:
    return g._result_is_lyrics(song)


@pytest.mark.parametrize(
    "song,expected",
    [
        pytest.param(
            {"lyrics_state": "incomplete", "title": "Some Song"},
            False,
            id="incomplete_lyrics_state",
        ),
        pytest.param(
            {"lyrics_state": "complete", "instrumental": True, "title": "Piano Solo"},
            False,
            id="instrumental_flag",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "Track List"},
            False,
            id="default_excluded_term",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "[Track List]"},
            False,
            id="default_excluded_term",
        ),
        pytest.param(
            {"lyrics_state": "complete", "title": "Hello World"},
            True,
            id="valid_song_title",
        ),
    ],
)
def test_result_is_lyrics_basic_cases(
    _result_is_lyrics_genius: Genius, song: dict[str, Any], expected: bool
) -> None:
    assert _call(_result_is_lyrics_genius, song) is expected


@pytest.mark.parametrize(
    "title,expected",
    [
        pytest.param("Bonus Track", False, id="excluded_via_custom_term"),
        pytest.param("Track List", False, id="default_term_still_excluded"),
        pytest.param("Tracklist", False, id="default_term_one_word_also_excluded"),
        pytest.param("Hello World", True, id="not_excluded"),
    ],
)
def test_custom_excluded_term_added_without_replacement(
    title: str, expected: bool
) -> None:
    g = Genius(
        verbose=False, excluded_terms=["bonus track"], replace_default_terms=False
    )
    assert _call(g, {"lyrics_state": "complete", "title": title}) is expected


@pytest.mark.parametrize(
    "title,expected",
    [
        pytest.param("Track List", True, id="default_term_no_longer_excluded"),
        pytest.param("Bonus Track", False, id="custom_term_still_excludes"),
        pytest.param("Song (Remix)", False, id="literal_parens_match_exactly"),
        pytest.param("Song Remix", True, id="without_parens_does_not_match"),
        pytest.param("Hello World", True, id="not_excluded"),
    ],
)
def test_replacing_default_terms_removes_original_exclusions(
    title: str, expected: bool
) -> None:
    g = Genius(
        verbose=False,
        excluded_terms=["bonus track", "(Remix)"],
        replace_default_terms=True,
    )
    assert _call(g, {"lyrics_state": "complete", "title": title}) is expected
