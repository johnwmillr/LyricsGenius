"""Tests for the official API methods and Genius helpers built on them."""

from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius

ANNOTATION_ID = 10225840
WEB_PAGE_ID = 10347
SONG_ID = 1
LYRICS_SONG_ID = 2885745
LYRICS_SONG_URL = "https://genius.com/Andy-shauf-begin-again-lyrics"


# Live only: the response is the token owner's private account data.
@pytest.mark.live
def test_account_returns_token_owner(live_genius: Genius) -> None:
    """The account endpoint returns the user that owns the access token."""
    response = live_genius.account()

    assert "id" in response["user"]


@pytest.mark.vcr
def test_annotation_returns_requested_annotation(genius: Genius) -> None:
    """Looking up an annotation by ID returns that annotation."""
    response = genius.annotation(ANNOTATION_ID)

    assert response["annotation"]["id"] == ANNOTATION_ID


@pytest.mark.skip(reason="creates and deletes a real annotation on the token's account")
def test_annotation_lifecycle(genius: Genius) -> None:
    """An annotation can be created, updated, voted on and deleted."""
    created = genius.create_annotation(
        "The annotation", "https://example.com", "illustrative examples", title="test"
    )["annotation"]
    try:
        assert created["body"]["plain"] == "The annotation"

        updated = genius.update_annotation(
            created["id"],
            "Updated annotation",
            "https://example.com",
            "illustrative examples",
            title="test",
        )["annotation"]
        assert updated["body"]["plain"] == "Updated annotation"

        assert genius.upvote_annotation(created["id"]) is not None
        assert genius.downvote_annotation(created["id"]) is not None
        assert genius.unvote_annotation(created["id"]) is not None
    finally:
        assert genius.delete_annotation(created["id"]) == 204


@pytest.mark.vcr
def test_referents_returns_web_page_referents(genius: Genius) -> None:
    """Referents for a web page all belong to that web page."""
    response = genius.referents(web_page_id=WEB_PAGE_ID)

    assert response["referents"]
    assert {r["annotatable"]["id"] for r in response["referents"]} == {WEB_PAGE_ID}


def test_referents_requires_an_item(genius: Genius) -> None:
    """Referents needs a song, web page or creator to look up."""
    with pytest.raises(AssertionError):
        genius.referents()


def test_referents_rejects_song_and_web_page_together(genius: Genius) -> None:
    """Referents accepts a song or a web page, not both."""
    with pytest.raises(AssertionError):
        genius.referents(song_id=1, web_page_id=1)


@pytest.mark.vcr
def test_web_page_returns_page_for_url(genius: Genius) -> None:
    """Looking up a web page by URL returns that page."""
    response = genius.web_page(raw_annotatable_url="https://docs.genius.com")

    assert response["web_page"]["id"] == WEB_PAGE_ID


@pytest.mark.vcr
def test_song_annotations_pairs_fragments_with_annotations(genius: Genius) -> None:
    """Song annotations pair each annotated fragment with its annotation bodies."""
    annotations = genius.song_annotations(SONG_ID)

    assert annotations
    for fragment, bodies in annotations:
        assert isinstance(fragment, str)
        assert fragment
        assert bodies
        assert all(isinstance(body, list) for body in bodies)


@pytest.mark.vcr
def test_tag_returns_first_page_of_songs(genius: Genius) -> None:
    """A tag page's songs are split into title, artists and featured artists."""
    response: dict[str, Any] = genius.tag("pop")

    assert response["next_page"] == 2
    assert len(response["hits"]) == 20
    for hit in response["hits"]:
        assert hit["url"].startswith("https://genius.com/")
        assert hit["title_with_artists"].startswith(hit["title"])
        assert "\xa0" not in hit["title_with_artists"]
        for name in hit["artists"] + hit["featured_artists"]:
            assert " & " not in name
            assert name in hit["title_with_artists"]
    by_title = {hit["title"]: hit for hit in response["hits"]}
    assert by_title["Despacito (Remix)"]["artists"] == ["Luis Fonsi", "Daddy Yankee"]
    assert by_title["Despacito (Remix)"]["featured_artists"] == ["Justin Bieber"]
    assert by_title["Starboy"]["artists"] == ["The Weeknd"]
    assert by_title["Starboy"]["featured_artists"] == ["Daft Punk"]


def test_search_song_requires_title_or_id(genius: Genius) -> None:
    """Searching for a song needs a title or a song ID."""
    with pytest.raises(AssertionError):
        genius.search_song()


@pytest.mark.live
def test_search_song_returns_song_with_lyrics(live_genius: Genius) -> None:
    """Searching by title and artist returns that song with its lyrics."""
    song = live_genius.search_song("99 Problems", "Jay-Z")

    assert song is not None
    assert song.title == "99 Problems"
    assert song.lyrics


@pytest.mark.live
def test_search_song_normalizes_whitespace(live_genius: Genius) -> None:
    """Extra whitespace in the title doesn't change which song is found."""
    song = live_genius.search_song("  \t 99  \t \t\tProblems   ", "Jay-Z")

    assert song is not None
    assert song.title == "99 Problems"


@pytest.mark.live
def test_search_song_by_id(live_genius: Genius) -> None:
    """Searching by song ID returns that song."""
    song = live_genius.search_song(song_id=LYRICS_SONG_ID)

    assert song is not None
    assert song.api_path == f"/songs/{LYRICS_SONG_ID}"


@pytest.mark.live
@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({"song_url": LYRICS_SONG_URL}, id="url"),
        pytest.param({"song_id": LYRICS_SONG_ID}, id="id"),
    ],
)
def test_lyrics_scrapes_song_page(live_genius: Genius, kwargs: dict[str, Any]) -> None:
    """Lyrics are scraped from the song page found by URL or ID."""
    lyrics = live_genius.lyrics(**kwargs)

    assert lyrics is not None
    assert lyrics.startswith("[Verse 1]")
    assert "[Outro]" in lyrics


def test_referents_accepts_creator_alone(genius: Genius) -> None:
    """Referents can be looked up by creator without a song or web page."""
    with mock.patch.object(
        genius, "_make_request", return_value={"referents": []}
    ) as request:
        genius.referents(created_by_id=7)

    params = request.call_args.kwargs["params_"]
    assert params["created_by_id"] == 7
    assert params["song_id"] is None
    assert params["web_page_id"] is None
