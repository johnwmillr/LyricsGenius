#  Command line usage:
#    python3 -m lyricsgenius --help
#    python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save
#    python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save

import argparse
import os

from . import Genius
from .utils import safe_unicode


def main(args=None):
    msg = "Download song lyrics from Genius.com"
    parser = argparse.ArgumentParser(prog="lyricsgenius", description=msg)
    positional = parser.add_argument_group("Required Arguments")
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

    optional = parser.add_argument_group("Optional Arguments")
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
    args = parser.parse_args()

    # Create an instance of the Genius class
    token = args.token if args.token else os.environ.get("GENIUS_ACCESS_TOKEN", None)
    if token is None:
        raise ValueError(
            "Must provide access token either as an argument or as an environment variable."
        )

    api = Genius(token, verbose=args.verbose, timeout=10)

    # Handle the command-line inputs
    if args.search_type == "song":
        song = api.search_song(*args.terms)
        if not song:
            if not args.quiet:
                print("Could not find specified song. Check spelling?")
            return
        for format in args.format:
            if not args.save:
                print(song.to_text() if format == "txt" else song.to_json())
            else:
                if not args.quiet:
                    print(
                        f"Saving lyrics to '{safe_unicode(song.title)}' in {format.upper()} format..."
                    )
                song.save_lyrics(
                    extension=format, overwrite=True if args.overwrite else False
                )
    elif args.search_type == "artist":
        artist = api.search_artist(
            args.terms[0], max_songs=args.max_songs, sort="popularity"
        )
        if not artist:
            if not args.quiet:
                print("Could not find specified artist. Check spelling?")
            return
        for format in args.format:
            if not args.save:
                print(artist.to_json() if format == "json" else artist.to_text())
            else:
                if not args.quiet:
                    print(
                        f"Saving '{safe_unicode(artist.name)}' lyrics in {format.upper()} format..."
                    )
                artist.save_lyrics(
                    extension=format, overwrite=True if args.overwrite else False
                )
    elif args.search_type == "album":
        album = api.search_album(*args.terms)
        if not album:
            if not args.quiet:
                print("Could not find specified album. Check spelling?")
            return
        if args.stdout:
            print(album.to_json() if args.stdout == "json" else album.to_text())
        if args.save:
            for format in args.save:
                if not args.quiet:
                    print(
                        f"Saving '{safe_unicode(album.name)}' lyrics in {format.upper()} format..."
                    )
                album.save_lyrics(
                    extension=format, overwrite=True if args.overwrite else False
                )


if __name__ == "__main__":
    main()
