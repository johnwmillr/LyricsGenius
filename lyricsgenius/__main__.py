#  Command line usage:
#    python3 -m lyricsgenius --help
#    python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save
#    python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save

import os
import argparse

from . import Genius
from .utils import safe_unicode


def main(args=None):
    msg = "Download song lyrics from Genius.com"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument(
        "search_type",
        type=str.lower,
        choices=["song", "artist", "album"],
        help="Specify whether search is for 'song', 'artist' or 'album'."
    )
    parser.add_argument("terms", type=str, nargs="+",
                        help="Provide terms for search")
    parser.add_argument("--save", type=str, nargs='?', const="json", choices=["json", "txt"],
                        help="Specify the format to save output: 'json' (default) or 'txt'")
    parser.add_argument("--max-songs", type=int,
                        help="Specify number of songs when searching for artist")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Turn off the API verbosity")
    args = parser.parse_args()

    # Create an instance of the Genius class
    access_token = os.environ.get("GENIUS_ACCESS_TOKEN", None)
    msg = "Must declare environment variable: GENIUS_ACCESS_TOKEN"
    assert access_token, msg
    api = Genius(access_token)
    if args.quiet:
        api.verbose = False

    # Handle the command-line inputs
    if args.search_type == "song":
        song = api.search_song(*args.terms)
        if not song:
            if not args.quiet:
                print("Could not find specified song. Check spelling?")
            return
        if args.save:
            if not args.quiet:
                print(f"Saving lyrics to '{safe_unicode(song.title)}' in {args.save.upper()} format...")
            song.save_lyrics(extension=args.save)
    elif args.search_type == "artist":
        artist = api.search_artist(args.terms[0],
                                   max_songs=args.max_songs,
                                   sort='popularity')
        if args.save:
            if not args.quiet:
                print(f"Saving '{safe_unicode(artist.name)}' lyrics in {args.save.upper()} format...")
            if args.save == "json":
                api.save_artists(artist, extension="json")
            elif args.save == "txt":
                api.save_artists(artist, extension="txt")
    elif args.search_type == "album":
        album = api.search_album(*args.terms)
        if args.save:
            if not args.quiet:
                print(f"Saving '{safe_unicode(album.name)}' lyrics in {args.save.upper()} format...")
            if args.save == "json":
                album.save_lyrics(extension="json")
            elif args.save == "txt":
                album.save_lyrics(extension="txt")


if __name__ == "__main__":
    main()
