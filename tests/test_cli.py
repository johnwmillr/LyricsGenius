from argparse import Namespace
from typing import cast
from unittest import mock

from lyricsgenius import Genius
from lyricsgenius.__main__ import Searcher


class _DummyAPI:
    def __init__(self, result: object | None) -> None:
        self.search_song = mock.Mock(return_value=result)
        self.search_artist = mock.Mock(return_value=result)
        self.search_album = mock.Mock(return_value=result)


def _args(save: bool, output_file: str | None = None) -> Namespace:
    return Namespace(
        terms=["Santa", "Madonna"],
        format=["json", "txt"],
        save=save,
        overwrite=True,
        output_file=output_file,
        max_songs=None,
    )


def test_searcher_passes_output_file_to_save_lyrics() -> None:
    result = mock.Mock()
    api = _DummyAPI(result)

    Searcher(cast(Genius, api), "song")(_args(save=True, output_file="custom_name"))

    assert result.save_lyrics.call_count == 2
    result.save_lyrics.assert_any_call(
        filename="custom_name", extension="json", overwrite=True
    )
    result.save_lyrics.assert_any_call(
        filename="custom_name", extension="txt", overwrite=True
    )


def test_searcher_uses_default_filename_when_output_file_is_none() -> None:
    result = mock.Mock()
    api = _DummyAPI(result)

    Searcher(cast(Genius, api), "song")(_args(save=True, output_file=None))

    assert result.save_lyrics.call_count == 2
    result.save_lyrics.assert_any_call(filename=None, extension="json", overwrite=True)
    result.save_lyrics.assert_any_call(filename=None, extension="txt", overwrite=True)


def test_searcher_prints_when_not_saving() -> None:
    result = mock.Mock()
    result.to_json.return_value = '{"ok": true}'
    result.to_text.return_value = "ok"
    api = _DummyAPI(result)

    with mock.patch("builtins.print") as print_mock:
        Searcher(cast(Genius, api), "song")(_args(save=False, output_file="ignored"))

    result.save_lyrics.assert_not_called()
    assert print_mock.call_count == 2
