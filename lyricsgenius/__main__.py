#  Command line usage:
#    python3 -m lyricsgenius --help
#    python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save
#    python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save

import os
import argparse

from lyricsgenius.api import Genius


def main(args=None):
    msg = "Download song lyrics from Genius.com"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("search_type", type=str.lower, choices=["song", "artist"],
                        help="Specify whether search is for 'song' or 'artist'")
    parser.add_argument("terms", type=str, nargs="+",
                        help="Provide terms for search")
    parser.add_argument("--save", action="store_true",
                        help="If specified, saves songs to JSON file")
    parser.add_argument("--max-songs", type=int,
                        help="Specify number of songs when searching for artist")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Turn off the API verbosity")
    parser.add_argument("-tl", "--tokenless", action="store_true",
                        help="Token-less Genius (makes the calls using the public API)")
    args = parser.parse_args()

    # Create an instance of the Genius class
    access_token = os.environ.get("GENIUS_ACCESS_TOKEN", None)
    api = Genius(access_token)
    if args.quiet:
        api.verbose = False
    if args.tokenless:
        api.public_api = True

    # Handle the command-line inputs
    if args.search_type == "song":
        song = api.search_song(*args.terms)
        if not song:
            if not args.quiet:
                print("Could not find specified song. Check spelling?")
            return
        if args.save:
            if not args.quiet:
                print("Saving lyrics to '{s}'...".format(s=song.title))
            song.save_lyrics()
    elif args.search_type == "artist":
        artist = api.search_artist(args.terms[0],
                                   max_songs=args.max_songs,
                                   sort='popularity')
        if args.save:
            if not args.quiet:
                print("Saving '{a}'' lyrics...".format(a=artist.name))
            api.save_artists(artist)
    elif args.search_type == "album":
        album = api.search_album(*args.terms)
        if args.save:
            if not args.quiet:
                print("Saving '{a}'' lyrics...".format(a=album.name))
            album.save_lyrics()


if __name__ == "__main__":
    main()
