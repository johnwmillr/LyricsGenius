"""Tests for the command line interface, with the Genius client mocked."""

import sys
from argparse import Namespace
from typing import Literal, cast
from unittest import mock

import pytest

from lyricsgenius import Genius
from lyricsgenius import __main__ as cli
from lyricsgenius.__main__ import Searcher

SearchType = Literal["song", "artist", "album"]


class _DummyAPI:
    """A stand-in client whose search methods each return their own result."""

    def __init__(self, found: bool = True) -> None:
        self.results = {
            name: mock.Mock(name=name) for name in ("song", "artist", "album")
        }
        self.search_song = mock.Mock(
            return_value=self.results["song"] if found else None
        )
        self.search_artist = mock.Mock(
            return_value=self.results["artist"] if found else None
        )
        self.search_album = mock.Mock(
            return_value=self.results["album"] if found else None
        )


def _args(
    save: bool = False,
    formats: list[str] | None = None,
    output_file: str | None = None,
    overwrite: bool = False,
    max_songs: int | None = None,
) -> Namespace:
    """Builds parsed CLI arguments for searching "Santa" by "Madonna"."""
    return Namespace(
        terms=["Santa", "Madonna"],
        format=formats or ["json", "txt"],
        save=save,
        overwrite=overwrite,
        output_file=output_file,
        max_songs=max_songs,
    )


@pytest.mark.parametrize("search_type", ["song", "album"])
def test_searcher_searches_by_type_with_the_terms(search_type: SearchType) -> None:
    """Only the search for the requested type runs, with the terms given."""
    api = _DummyAPI()

    Searcher(cast(Genius, api), search_type)(_args(save=True))

    for name in ("song", "artist", "album"):
        search = getattr(api, f"search_{name}")
        if name == search_type:
            search.assert_called_once_with("Santa", "Madonna")
        else:
            search.assert_not_called()


def test_searcher_passes_max_songs_to_artist_search() -> None:
    """An artist search is limited to --max-songs songs."""
    api = _DummyAPI()

    Searcher(cast(Genius, api), "artist")(_args(save=True, max_songs=3))

    api.search_artist.assert_called_once_with("Santa", "Madonna", max_songs=3)
    api.search_song.assert_not_called()


def test_searcher_rejects_unknown_search_type() -> None:
    """A search type other than song, artist or album is rejected."""
    with pytest.raises(ValueError, match="Unknown search type"):
        Searcher(cast(Genius, _DummyAPI()), cast(SearchType, "playlist"))


@pytest.mark.parametrize("overwrite", [True, False])
def test_searcher_saves_each_format(overwrite: bool) -> None:
    """With --save, the result is saved once per format with the CLI's options."""
    api = _DummyAPI()

    Searcher(cast(Genius, api), "song")(
        _args(save=True, output_file="custom_name", overwrite=overwrite)
    )

    assert api.results["song"].save_lyrics.call_args_list == [
        mock.call(filename="custom_name", extension="json", overwrite=overwrite),
        mock.call(filename="custom_name", extension="txt", overwrite=overwrite),
    ]


def test_searcher_prints_each_format_in_order() -> None:
    """Without --save, each format is printed in the order given."""
    api = _DummyAPI()
    result = api.results["song"]
    result.to_json.return_value = '{"ok": true}'
    result.to_text.return_value = "ok"

    with mock.patch("builtins.print") as print_:
        Searcher(cast(Genius, api), "song")(_args(formats=["json", "txt"]))

    result.save_lyrics.assert_not_called()
    assert print_.call_args_list == [mock.call('{"ok": true}'), mock.call("ok")]


def test_searcher_does_nothing_without_a_result() -> None:
    """When nothing is found, nothing is printed or saved."""
    api = _DummyAPI(found=False)

    with mock.patch("builtins.print") as print_:
        Searcher(cast(Genius, api), "song")(_args())

    print_.assert_not_called()


def _run_main(monkeypatch: pytest.MonkeyPatch, *argv: str) -> mock.Mock:
    """Runs main() with the arguments and returns the mocked Genius class."""
    monkeypatch.setattr(sys, "argv", ["lyricsgenius", *argv])
    genius_class = mock.Mock(return_value=_DummyAPI())
    monkeypatch.setattr(cli, "Genius", genius_class)
    cli.main()
    return genius_class


def test_main_saves_search_result_with_options(monkeypatch: pytest.MonkeyPatch) -> None:
    """main() searches with the parsed terms and saves with the parsed options."""
    monkeypatch.setenv("GENIUS_ACCESS_TOKEN", "env_token")

    genius_class = _run_main(
        monkeypatch,
        "SONG",
        "Santa",
        "Madonna",
        "-f",
        "JSON",
        "-s",
        "--output-file",
        "out",
    )

    genius_class.assert_called_once_with("env_token", timeout=10)
    api = genius_class.return_value
    api.search_song.assert_called_once_with("Santa", "Madonna")
    api.results["song"].save_lyrics.assert_called_once_with(
        filename="out", extension="json", overwrite=False
    )


def test_main_prefers_token_argument(monkeypatch: pytest.MonkeyPatch) -> None:
    """--token takes precedence over GENIUS_ACCESS_TOKEN."""
    monkeypatch.setenv("GENIUS_ACCESS_TOKEN", "env_token")

    with mock.patch("builtins.print"):
        genius_class = _run_main(monkeypatch, "song", "Santa", "-t", "arg_token")

    genius_class.assert_called_once_with("arg_token", timeout=10)


def test_main_requires_a_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """main() refuses to run without a token from --token or the environment."""
    monkeypatch.delenv("GENIUS_ACCESS_TOKEN", raising=False)

    with pytest.raises(ValueError, match="access token"):
        _run_main(monkeypatch, "song", "Santa")
