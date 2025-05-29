import argparse
import os
from typing import Callable, Literal

from . import Genius
from .types import Album, Artist, Song

SearchResult = Song | Artist | Album


class Searcher:
    """Executes the search specified by the CLI args"""

    def __init__(
        self, api: Genius, search_type: Literal["song", "artist", "album"]
    ) -> None:
        self.api = api
        self.search_type = search_type
        self.search_func: Callable[..., SearchResult | None]

        match search_type:
            case "song":
                self.search_func = api.search_song
            case "artist":
                self.search_func = api.search_artist
            case "album":
                self.search_func = api.search_album
            case _:
                raise ValueError(f"Unknown search type: {search_type}")

    def __call__(self, args: argparse.Namespace) -> None:
        kwargs = {"max_songs": args.max_songs} if self.search_type == "artist" else {}
        if not (result := self.search_func(*args.terms, **kwargs)):
            return

        for format in args.format:
            if not args.save:
                print(result.to_text() if format == "txt" else result.to_json())
            else:
                if args.verbose:
                    print(f"Saving lyrics in {format.upper()} format.")
                result.save_lyrics(extension=format, overwrite=args.overwrite)


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="lyricsgenius", description="Download song lyrics from Genius.com"
    )
    positional: argparse._ArgumentGroup = parser.add_argument_group(
        "Required Arguments"
    )
    positional.add_argument(
        "search_type",
        type=str.lower,
        choices=["song", "artist", "album"],
        help="Specify whether search is for 'song', 'artist' or 'album'.",
    )
    positional.add_argument(
        "terms",
        type=str,
        nargs="+",
        help="Provide terms for the search (e.g. 'All You Need Is Love' 'The Beatles').",
    )

    optional: argparse._ArgumentGroup = parser.add_argument_group("Optional Arguments")
    optional.add_argument(
        "-f",
        "--format",
        type=str.lower,
        nargs="+",
        default=["txt"],
        choices=["txt", "json"],
        help="Specify output format(s): 'txt' (default) or 'json'. You can specify multiple formats.",
    )
    optional.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Save the lyrics to a file in the specified format instead of printing to stdout",
    )
    optional.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite the file if it already exists",
    )
    optional.add_argument(
        "-n",
        "--max-songs",
        type=int,
        help="Specify number of songs when searching for artist",
    )
    optional.add_argument(
        "-t",
        "--token",
        type=str,
        default=None,
        help="Specify your Genius API access token (optional). If not provided, it will be read from the GENIUS_ACCESS_TOKEN environment variable.",
    )
    optional.add_argument(
        "-v", "--verbose", action="store_true", help="Turn on the API verbosity"
    )
    args: argparse.Namespace = parser.parse_args()

    # Create an instance of the Genius class
    token: str | None = (
        args.token if args.token else os.environ.get("GENIUS_ACCESS_TOKEN", None)
    )
    if token is None:
        raise ValueError(
            "Must provide access token either as an argument or as an environment variable."
        )

    api = Genius(token, verbose=args.verbose, timeout=10)
    Searcher(api, args.search_type)(args)


if __name__ == "__main__":
    main()
