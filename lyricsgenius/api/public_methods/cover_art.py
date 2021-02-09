class CoverArtMethods(object):
    """Cover art methods of the public API."""

    def cover_arts(self, album_id=None, song_id=None, text_format=None):
        """Gets the cover arts of an album or a song.

        You must supply one of :obj:`album_id` or :obj:`song_id`.

        Args:
            album_id (:obj:`int`, optional): Genius album ID
            song_id (:obj:`int`, optional): Genius song ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain'). Defines the text
                formatting for the annotation of the cover arts,
                if there are any.

        Returns:
            :obj:`dict`

        """
        msg = "Must supply `album_id` or `song_id`."
        assert any([album_id, song_id]), msg
        msg = ("Pass only one of `album_id` or `song_id`"
               ", not both.")
        condition = (
            sum([bool(album_id), bool(song_id)])
            == 1
        )
        assert condition, msg
        endpoint = 'cover_arts'
        params = {'text_format': text_format or self.response_format}
        if album_id is not None:
            params['album_id'] = album_id
        else:
            params['song_id'] = song_id
        return self._make_request(path=endpoint, params_=params, public_api=True)
