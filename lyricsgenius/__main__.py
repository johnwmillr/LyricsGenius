#  Command line usage:
#    python3 -m lyricsgenius --help
#    python3 -m lyricsgenius song "Begin Again" "Andy Shauf" --save
#    python3 -m lyricsgenius artist "The Beatles" --max-songs 5 --save

import os
import argparse
import logging

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
    parser.add_argument("--save", action="store_true",
                        help="If specified, saves songs to JSON file")
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
    api._cli = True
    if args.quiet:
        log_level = logging.NOTSET
    else:
        log_level = logging.INFO
    # Set up logging
    logging.basicConfig(format="%(message)s")
    logger = logging.getLogger(__package__)
    logger.setLevel(log_level)

    # Handle the command-line inputs
    if args.search_type == "song":
        song = api.search_song(*args.terms)
        if not song:
            logger.info("Could not find specified song. Check spelling?")
            return
        if args.save:
            logger.info("Saving lyrics to '%s'...", safe_unicode(song.title))
            song.save_lyrics()
    elif args.search_type == "artist":
        artist = api.search_artist(args.terms[0],
                                   max_songs=args.max_songs,
                                   sort='popularity')
        if args.save:
            logger.info("Saving '%s' lyrics...", safe_unicode(artist.name))
            api.save_artists(artist)
    elif args.search_type == "album":
        album = api.search_album(*args.terms)
        if args.save:
            logger.info("Saving '%s' lyrics...", safe_unicode(album.name))
            album.save_lyrics()


if __name__ == "__main__":
    main()
