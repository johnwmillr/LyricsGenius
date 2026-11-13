"""Tests for the PublicAPI methods, replayed from recorded genius.com/api responses."""

import inspect
from typing import Any

import pytest
from requests.exceptions import HTTPError

from lyricsgenius import Genius, PublicAPI

ALBUM_ID = 104614
ANNOTATION_ID = 10225840
ARTICLE_ID = 11880
ARTIST_ID = 1665
SONG_ID = 378195
USER_ID = 1
VIDEO_ID = 18681
WEB_PAGE_ID = 10347
REFERENT_IDS = [20793764, 20641014]
COMMENTED_ANNOTATION_ID = 2941046
PER_PAGE = 2

# Methods whose endpoints return a fixed page size whatever per_page says.
_IGNORES_PER_PAGE = {"artist_activity", "search_artist_songs"}

# Recorded 2026-11-13: genius.com/api/page_data returned 404 for every page
# path tried, including the documented album and song forms.
_PAGE_DATA_REMOVED = pytest.mark.xfail(
    raises=HTTPError,
    strict=True,
    reason="Genius no longer serves page_data; every page path returns 404",
)


# Sent to every method that accepts them. They differ from the defaults, so
# each recorded request pins the names of the parameters the method sends.
_OPTIONAL_PARAMS: dict[str, Any] = {
    "per_page": PER_PAGE,
    "page": 1,
    "text_format": "html",
}


def _accepts(client: PublicAPI, method: str, param: str) -> bool:
    """Reports whether a method takes the given parameter."""
    return param in inspect.signature(getattr(client, method)).parameters


def _call(client: PublicAPI, method: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Calls a method with its arguments plus any optional parameters it takes."""
    optional = {
        name: value
        for name, value in _OPTIONAL_PARAMS.items()
        if name not in kwargs and _accepts(client, method, name)
    }
    response: dict[str, Any] = getattr(client, method)(**kwargs, **optional)
    return response


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("method", "id_"),
    [
        pytest.param("album", ALBUM_ID, id="album"),
        pytest.param("annotation", ANNOTATION_ID, id="annotation"),
        pytest.param("article", ARTICLE_ID, id="article"),
        pytest.param("artist", ARTIST_ID, id="artist"),
        pytest.param("song", SONG_ID, id="song"),
        pytest.param("user", USER_ID, id="user"),
        pytest.param("video", VIDEO_ID, id="video"),
    ],
)
def test_lookup_returns_requested_item(
    public_api: PublicAPI, method: str, id_: int
) -> None:
    """Looking up an item by ID returns that item."""
    response = _call(public_api, method, {f"{method}_id": id_})

    assert response[method]["id"] == id_


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("method", "kwargs", "key"),
    [
        pytest.param("albums_charts", {}, "chart_items", id="albums_charts"),
        pytest.param(
            "album_comments", {"album_id": ALBUM_ID}, "comments", id="album_comments"
        ),
        pytest.param(
            "album_cover_arts",
            {"album_id": ALBUM_ID},
            "cover_arts",
            id="album_cover_arts",
        ),
        pytest.param(
            "album_leaderboard",
            {"album_id": ALBUM_ID},
            "leaderboard",
            id="album_leaderboard",
        ),
        pytest.param(
            "album_tracks", {"album_id": ALBUM_ID}, "tracks", id="album_tracks"
        ),
        pytest.param(
            "annotation_edits",
            {"annotation_id": ANNOTATION_ID},
            "versions",
            id="annotation_edits",
        ),
        pytest.param(
            "annotation_comments",
            {"annotation_id": COMMENTED_ANNOTATION_ID},
            "comments",
            id="annotation_comments",
        ),
        pytest.param(
            "article_comments",
            {"article_id": ARTICLE_ID},
            "comments",
            id="article_comments",
        ),
        pytest.param(
            "latest_articles", {}, "editorial_placements", id="latest_articles"
        ),
        pytest.param(
            "artist_activity",
            {"artist_id": ARTIST_ID},
            "line_items",
            id="artist_activity",
        ),
        pytest.param(
            "artist_albums", {"artist_id": ARTIST_ID}, "albums", id="artist_albums"
        ),
        pytest.param(
            "artist_followers",
            {"artist_id": ARTIST_ID},
            "followers",
            id="artist_followers",
        ),
        pytest.param(
            "artist_leaderboard",
            {"artist_id": ARTIST_ID},
            "leaderboard",
            id="artist_leaderboard",
        ),
        pytest.param(
            "artist_songs", {"artist_id": ARTIST_ID}, "songs", id="artist_songs"
        ),
        pytest.param(
            "search_artist_songs",
            {"artist_id": ARTIST_ID, "search_term": "bad"},
            "songs",
            id="search_artist_songs",
        ),
        pytest.param(
            "cover_arts",
            {"song_id": SONG_ID},
            "cover_arts",
            id="cover_arts_song",
            marks=pytest.mark.xfail(
                raises=HTTPError,
                strict=True,
                reason="Genius now requires album_id: 400 'must include one of: album_id'",
            ),
        ),
        pytest.param("discussions", {}, "discussions", id="discussions"),
        pytest.param("leaderboard", {}, "leaderboard", id="leaderboard"),
        pytest.param("charts", {}, "chart_items", id="charts"),
        pytest.param("questions", {"album_id": ALBUM_ID}, "questions", id="questions"),
        pytest.param(
            "questions", {"song_id": SONG_ID}, "questions", id="questions_song"
        ),
        pytest.param(
            "referents", {"web_page_id": WEB_PAGE_ID}, "referents", id="referents"
        ),
        pytest.param("referents_charts", {}, "chart_items", id="referents_charts"),
        pytest.param("search", {"search_term": "test"}, "hits", id="search"),
        pytest.param(
            "song_activity", {"song_id": SONG_ID}, "line_items", id="song_activity"
        ),
        pytest.param(
            "song_comments", {"song_id": SONG_ID}, "comments", id="song_comments"
        ),
        pytest.param(
            "song_contributors",
            {"song_id": SONG_ID},
            "contributors",
            id="song_contributors",
        ),
        pytest.param(
            "user_accomplishments",
            {"user_id": USER_ID},
            "accomplishments",
            id="user_accomplishments",
        ),
        pytest.param(
            "user_following",
            {"user_id": USER_ID},
            "followed_users",
            id="user_following",
        ),
        pytest.param(
            "user_followers", {"user_id": USER_ID}, "followers", id="user_followers"
        ),
        pytest.param(
            "user_contributions",
            # Genius returns no groups for small page sizes, such as 2.
            {"user_id": USER_ID, "per_page": 20},
            "contribution_groups",
            id="user_contributions",
        ),
        pytest.param("videos", {"video_id": VIDEO_ID}, "videos", id="videos"),
        pytest.param("videos", {"song_id": SONG_ID}, "videos", id="videos_song"),
        pytest.param("videos", {"album_id": ALBUM_ID}, "videos", id="videos_album"),
        pytest.param(
            "videos",
            {"video_id": VIDEO_ID, "series": True},
            "video_lists",
            id="videos_series",
        ),
        pytest.param("voters", {"annotation_id": ANNOTATION_ID}, "voters", id="voters"),
    ],
)
def test_response_contains_expected_key(
    public_api: PublicAPI, method: str, kwargs: dict[str, Any], key: str
) -> None:
    """Each method returns results under its key, at most per_page of them."""
    response = _call(public_api, method, kwargs)

    results = response[key]
    assert results
    if (
        isinstance(results, list)
        and _accepts(public_api, method, "per_page")
        and method not in _IGNORES_PER_PAGE
    ):
        assert len(results) <= kwargs.get("per_page", PER_PAGE)


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("method", "section_type"),
    [
        pytest.param("search_albums", "album", id="albums"),
        pytest.param("search_articles", "article", id="articles"),
        pytest.param("search_artists", "artist", id="artists"),
        pytest.param("search_lyrics", "lyric", id="lyrics"),
        pytest.param("search_songs", "song", id="songs"),
        pytest.param("search_users", "user", id="users"),
        pytest.param("search_videos", "video", id="videos"),
        pytest.param("search_all", "top_hit", id="all"),
    ],
)
def test_typed_search_returns_matching_section(
    public_api: PublicAPI, method: str, section_type: str
) -> None:
    """A typed search returns results in a section of that type first."""
    response = _call(public_api, method, {"search_term": "test"})

    assert response["sections"][0]["type"] == section_type


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("method", "contribution_type"),
    [
        pytest.param("user_annotations", "annotation", id="annotations"),
        pytest.param("user_articles", "article", id="articles"),
        pytest.param("user_pyongs", "pyong", id="pyongs"),
        pytest.param(
            "user_questions_and_answers", "answer", id="questions_and_answers"
        ),
        pytest.param("user_suggestions", "comment", id="suggestions"),
        pytest.param("user_transcriptions", "song", id="transcriptions"),
        pytest.param("user_unreviewed", "annotation", id="unreviewed"),
    ],
)
def test_user_contributions_are_filtered_by_type(
    public_api: PublicAPI, method: str, contribution_type: str
) -> None:
    """Each user contribution method returns contributions of its type."""
    response = _call(public_api, method, {"user_id": USER_ID})

    assert response["contribution_groups"][0]["contribution_type"] == contribution_type


@pytest.mark.vcr
def test_referent_returns_each_requested_referent(public_api: PublicAPI) -> None:
    """Looking up several referents returns all of them, keyed by ID."""
    response = public_api.referent(REFERENT_IDS)

    assert {str(id_) for id_ in REFERENT_IDS} <= response["referents"].keys()


@pytest.mark.vcr
@_PAGE_DATA_REMOVED
def test_page_data_returns_album_page_data(genius: Genius) -> None:
    """Page data for an album path contains the album's page data."""
    response = genius.page_data(album="/albums/Eminem/Music-to-be-murdered-by")

    assert "page_data" in response


@pytest.mark.vcr
@_PAGE_DATA_REMOVED
def test_page_data_returns_song_page_data(
    genius: Genius, public_api: PublicAPI
) -> None:
    """Page data for an artist slug and song path contains the song's page data."""
    artist_slug = public_api.artist(ARTIST_ID)["artist"]["slug"]
    song_path = genius.song(4558484)["song"]["path"]

    response = genius.page_data(artist=artist_slug, song=song_path)

    assert "page_data" in response


@pytest.mark.parametrize(
    ("method", "kwargs", "reason"),
    [
        pytest.param(
            "artist_contribution_opportunities",
            {"artist_id": ARTIST_ID},
            "requires a logged in user",
            id="artist_contribution_opportunities",
        ),
        pytest.param(
            "line_item",
            {"line_item_id": 323922396},
            "requires a logged in user",
            id="line_item",
        ),
        pytest.param("discussion", {"discussion_id": 524671}, "403", id="discussion"),
        pytest.param(
            "discussion_replies",
            {"discussion_id": 524671},
            "403",
            id="discussion_replies",
        ),
    ],
)
def test_unsupported_method_raises_not_implemented(
    public_api: PublicAPI, method: str, kwargs: dict[str, Any], reason: str
) -> None:
    """Methods Genius doesn't serve to anonymous clients raise, saying why."""
    with pytest.raises(NotImplementedError, match=reason):
        _call(public_api, method, kwargs)
