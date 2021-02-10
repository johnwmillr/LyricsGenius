# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

from filecmp import cmp

from .base import BaseEntity, Stats
from .artist import Artist


class Song(BaseEntity):
    """A song from the Genius.com database."""

    def __init__(self, client, json_dict, lyrics=""):
        body = json_dict
        super().__init__(body['id'])
        self._body = body
        self._client = client
        self.artist = body['primary_artist']['name']
        self.lyrics = lyrics if lyrics else ""
        self.primary_artist = Artist(client, body['primary_artist'])
        self.stats = Stats(body['stats'])

        self.annotation_count = body['annotation_count']
        self.api_path = body['api_path']
        self.apple_music_id = body.get('apple_music_id')
        self.apple_music_player_url = body.get('apple_music_player_url')
        self.description = body.get('description')
        self.embed_content = body.get('embed_content')
        self.featured_video = body.get('featured_video')
        self.full_title = body['full_title']
        self.header_image_thumbnail_url = body['header_image_thumbnail_url']
        self.header_image_url = body['header_image_url']
        self.lyrics_owner_id = body['lyrics_owner_id']
        self.lyrics_placeholder_reason = body.get('lyrics_placeholder_reason')
        self.lyrics_state = body['lyrics_state']
        self.path = body['path']
        self.pyongs_count = body['pyongs_count']
        self.recording_location = body.get('recording_location')
        self.release_date = body.get('release_date')
        self.release_date_for_display = body.get('release_date_for_display')
        self.song_art_image_thumbnail_url = body['song_art_image_thumbnail_url']
        self.song_art_image_url = body['song_art_image_url']
        self.title = body['title']
        self.title_with_featured = body['title_with_featured']
        self.url = body['url']

        # TODO: Create types for the following keys
        self.custom_performances = body.get("custom_performances")
        self.description_annotation = body.get("description_annotation")
        self.featured_artists = body.get("featured_artists")
        self.lyrics_marked_complete_by = body.get("lyrics_marked_complete_by")
        self.media = body.get("media")
        producer_artists = body.get("producer_artists")
        if isinstance(producer_artists, list):
            producer_artists = list(map(lambda a: Artist(client, a), producer_artists))
        self.producer_artists = producer_artists
        self.song_relationships = body.get("song_relationships")
        self.verified_annotations_by = body.get("verified_annotations_by")
        self.verified_contributors = body.get("verified_contributors")
        self.verified_lyrics_by = body.get("verified_lyrics_by")

    def to_dict(self):
        body = super().to_dict()
        body['artist'] = self.artist
        body['lyrics'] = self.lyrics
        return body

    def to_json(self,
                filename=None,
                sanitize=True,
                ensure_ascii=True):
        data = self.to_dict()
        return super().to_json(data=data,
                               filename=filename,
                               sanitize=sanitize,
                               ensure_ascii=ensure_ascii)

    def to_text(self,
                filename=None,
                sanitize=True):
        data = self.lyrics

        return super().to_text(data=data,
                               filename=filename,
                               sanitize=sanitize)

    def save_lyrics(self,
                    filename=None,
                    extension='json',
                    overwrite=False,
                    ensure_ascii=True,
                    sanitize=True,
                    verbose=True):

        if filename is None:
            filename = "Lyrics_{}_{}".format(self.artist.replace(" ", ""),
                                             self.title.replace(" ", "")
                                             ).lower()

        return super().save_lyrics(filename=filename,
                                   extension=extension,
                                   overwrite=overwrite,
                                   ensure_ascii=ensure_ascii,
                                   sanitize=sanitize,
                                   verbose=verbose)

    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else:
            lyr = self.lyrics[:100]
        return '"{title}" by {artist}:\n    {lyrics}'.format(
            title=self.title, artist=self.artist, lyrics=lyr.replace('\n', '\n    '))

    def __cmp__(self, other):
        return (cmp(self.title, other.title)
                and cmp(self.artist, other.artist)
                and cmp(self.lyrics, other.lyrics))
