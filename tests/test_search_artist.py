"""Tests for search_artist: finding the artist and collecting their songs."""

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from unittest import mock

import pytest

from lyricsgenius import Genius


def _artist_hit(id_: int, name: str) -> dict[str, Any]:
    """Builds an artist search hit."""
    return {"index": "artist", "result": {"id": id_, "name": name}}


def _search_response(artist_hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Builds a search_all response whose artist section holds the given hits."""
    return {
        "sections": [
            # The first section is read as the top hits.
            {"type": "top_hits", "hits": artist_hits[:1]},
            {"type": "artist", "hits": artist_hits},
            {"type": "song", "hits": []},
        ]
    }


def _artist_info(id_: int, name: str) -> dict[str, Any]:
    """Builds the minimal artist response the Artist type accepts."""
    return {
        "artist": {
            "id": id_,
            "name": name,
            "url": f"https://genius.com/artists/{name.replace(' ', '-')}",
            "api_path": f"/artists/{id_}",
            "header_image_url": "https://example.com/header.jpg",
            "image_url": "https://example.com/image.jpg",
            "is_meme_verified": False,
            "is_verified": False,
        }
    }


@contextmanager
def _mocked_search(
    genius: Genius, pages: list[dict[str, Any]], artist: dict[str, Any] | None = None
) -> Iterator[tuple[mock.Mock, mock.Mock]]:
    """Serves the pages from search_all in order and the artist from artist()."""
    with (
        mock.patch.object(genius, "search_all", side_effect=pages) as search_all,
        mock.patch.object(genius, "artist", return_value=artist) as artist_lookup,
        mock.patch.object(
            genius, "artist_songs", return_value={"songs": [], "next_page": None}
        ),
    ):
        yield search_all, artist_lookup


@pytest.mark.parametrize("per_page", [0, -1, 6, 50, 100])
def test_genius_rejects_out_of_range_per_page(per_page: int) -> None:
    """per_page outside 1 to 5 is rejected, since search_all can't serve it."""
    with pytest.raises(ValueError, match="per_page must be between 1 and 5"):
        Genius("dummy_token", sleep_time=0, per_page=per_page)


@pytest.mark.parametrize("per_page", [1, 2, 3, 4, 5])
def test_genius_accepts_per_page_from_one_to_five(per_page: int) -> None:
    """per_page from 1 to 5 is kept as given."""
    client = Genius("dummy_token", sleep_time=0, per_page=per_page)

    assert client.per_page == per_page


def test_search_artist_finds_exact_match_on_a_later_page(genius: Genius) -> None:
    """Paging continues past a full page without an exact match."""
    pages = [
        _search_response(
            [_artist_hit(i, f"Radiohead Tribute {i}") for i in range(1, 6)]
        ),
        _search_response([_artist_hit(99, "Radiohead")]),
    ]

    with _mocked_search(genius, pages, _artist_info(99, "Radiohead")) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 2
    artist_lookup.assert_called_once_with(99)
    assert artist is not None
    assert artist.name == "Radiohead"


def test_search_artist_falls_back_to_first_page_result(genius: Genius) -> None:
    """Without an exact match, the best result from the first page is used."""
    pages = [
        _search_response(
            [
                _artist_hit(1, "Radiohead Tribute"),
                *[_artist_hit(i, f"Radiohead Fan {i}") for i in range(2, 6)],
            ]
        ),
        _search_response([_artist_hit(99, "Radiohead something else")]),
    ]

    with _mocked_search(genius, pages, _artist_info(1, "Radiohead Tribute")) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 2
    artist_lookup.assert_called_once_with(1)
    assert artist is not None
    assert artist.name == "Radiohead Tribute"


def test_search_artist_stops_when_no_artists_are_found(genius: Genius) -> None:
    """An empty artist section ends the search with no artist."""
    with _mocked_search(genius, [_search_response([])]) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 1
    artist_lookup.assert_not_called()
    assert artist is None


def test_search_artist_stops_after_a_partial_page(genius: Genius) -> None:
    """A page that isn't full is the last one, so no further page is requested."""
    pages = [_search_response([_artist_hit(1, "Radiohead Fan")])]

    with _mocked_search(genius, pages, _artist_info(1, "Radiohead Fan")) as mocks:
        artist = genius.search_artist("Radiohead", max_songs=0)

    search_all, artist_lookup = mocks
    assert search_all.call_count == 1
    artist_lookup.assert_called_once_with(1)
    assert artist is not None
    assert artist.name == "Radiohead Fan"


def test_search_artist_stops_after_ten_pages(genius: Genius) -> None:
    """Paging stops after ten full pages even if none has an exact match."""
    full_page = _search_response(
        [_artist_hit(i, f"Radiohead Clone {i}") for i in range(5)]
    )

    with _mocked_search(
        genius, [full_page] * 11, _artist_info(0, "Radiohead Clone 0")
    ) as mocks:
        genius.search_artist("Radiohead", max_songs=0)

    search_all, _ = mocks
    assert search_all.call_count == 10


ARTIST_ID = 7
ARTIST_NAME = "Py Testerson"


def _song(
    id_: int,
    title: str,
    artist: str = ARTIST_NAME,
    lyrics_state: str = "complete",
    featured: list[str] | None = None,
) -> dict[str, Any]:
    """Builds a song entry as artist_songs returns it."""
    return {
        "id": id_,
        "title": title,
        "primary_artist": {"name": artist},
        "featured_artists": [{"name": name} for name in featured or []],
        "lyrics_state": lyrics_state,
        "url": f"https://genius.com/song-{id_}",
    }


def _page(songs: list[dict[str, Any]], next_page: int | None) -> dict[str, Any]:
    """Builds one page of artist_songs results."""
    return {"songs": songs, "next_page": next_page}


@contextmanager
def _mocked_songs(
    genius: Genius, pages: list[dict[str, Any]]
) -> Iterator[tuple[mock.Mock, mock.Mock, mock.Mock]]:
    """Serves the artist, the pages of songs, and lyrics named after each URL."""
    with (
        mock.patch.object(
            genius, "artist", return_value=_artist_info(ARTIST_ID, ARTIST_NAME)
        ),
        mock.patch.object(genius, "artist_songs", side_effect=pages) as artist_songs,
        mock.patch.object(
            genius, "lyrics", side_effect=lambda song_url: f"lyrics of {song_url}"
        ) as lyrics,
        mock.patch.object(
            genius, "song", side_effect=lambda id_: {"song": {"full_info": id_}}
        ) as song,
    ):
        yield artist_songs, lyrics, song


def test_search_artist_collects_valid_songs_across_pages(genius: Genius) -> None:
    """Songs are gathered from every page, skipping non-songs and other artists."""
    pages = [
        _page([_song(1, "First"), _song(2, "Tracklist")], next_page=2),
        _page([_song(3, "Second"), _song(4, "Theirs", artist="Someone Else")], None),
    ]

    with _mocked_songs(genius, pages) as (artist_songs, _, _):
        artist = genius.search_artist(
            ARTIST_NAME,
            artist_id=ARTIST_ID,
            sort="title",
            per_page=7,
            get_full_info=False,
        )

    assert artist is not None
    assert artist_songs.call_args_list == [
        mock.call(artist_id=ARTIST_ID, per_page=7, page=1, sort="title"),
        mock.call(artist_id=ARTIST_ID, per_page=7, page=2, sort="title"),
    ]
    assert [song.title for song in artist.songs] == ["First", "Second"]
    assert [song.lyrics for song in artist.songs] == [
        "lyrics of https://genius.com/song-1",
        "lyrics of https://genius.com/song-3",
    ]


def test_search_artist_stops_at_max_songs(genius: Genius) -> None:
    """Collection stops once max_songs songs are added, without the next page."""
    pages = [
        _page([_song(1, "First"), _song(2, "Second")], next_page=2),
        _page([_song(3, "Third")], next_page=None),
    ]

    with _mocked_songs(genius, pages) as (artist_songs, lyrics, _):
        artist = genius.search_artist(
            ARTIST_NAME, artist_id=ARTIST_ID, max_songs=1, get_full_info=False
        )

    assert artist is not None
    assert [song.title for song in artist.songs] == ["First"]
    assert artist_songs.call_count == 1
    assert lyrics.call_count == 1


def test_search_artist_skips_lyrics_request_for_incomplete_songs(
    genius: Genius,
) -> None:
    """A song whose lyrics aren't complete is kept with empty lyrics, unfetched."""
    genius.skip_non_songs = False
    pages = [_page([_song(1, "Unreleased", lyrics_state="unreleased")], None)]

    with _mocked_songs(genius, pages) as (_, lyrics, _):
        artist = genius.search_artist(
            ARTIST_NAME, artist_id=ARTIST_ID, get_full_info=False
        )

    assert artist is not None
    assert [song.lyrics for song in artist.songs] == [""]
    lyrics.assert_not_called()


def test_search_artist_merges_full_song_info(genius: Genius) -> None:
    """With get_full_info, each song's full data is fetched by ID and merged in."""
    pages = [_page([_song(1, "First"), _song(3, "Second")], None)]

    with _mocked_songs(genius, pages) as (_, _, song):
        artist = genius.search_artist(ARTIST_NAME, artist_id=ARTIST_ID)

    assert artist is not None
    assert song.call_args_list == [mock.call(1), mock.call(3)]
    assert [s._body["full_info"] for s in artist.songs] == [1, 3]


@pytest.mark.parametrize(
    ("include_features", "titles"),
    [
        pytest.param(True, ["Own", "Featured On"], id="included"),
        pytest.param(False, ["Own"], id="excluded"),
    ],
)
def test_search_artist_includes_features_only_when_asked(
    genius: Genius, include_features: bool, titles: list[str]
) -> None:
    """Songs that only feature the artist are kept only with include_features."""
    pages = [
        _page(
            [
                _song(1, "Own"),
                _song(2, "Featured On", artist="Headliner", featured=[ARTIST_NAME]),
            ],
            None,
        )
    ]

    with _mocked_songs(genius, pages):
        artist = genius.search_artist(
            ARTIST_NAME,
            artist_id=ARTIST_ID,
            include_features=include_features,
            get_full_info=False,
        )

    assert artist is not None
    assert [song.title for song in artist.songs] == titles
