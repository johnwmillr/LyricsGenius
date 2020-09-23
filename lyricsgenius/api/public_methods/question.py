class QuestionMethods(object):
    """Question methods of the public API."""

    def questions(self,
                  album_id=None,
                  song_id=None,
                  per_page=None,
                  page=None,
                  state=None,
                  text_format=None):
        """Gets the questions on an album or a song.
        You must supply one of :obj:`album_id` or :obj:`song_id`.

        Args:
            time_period (:obj:`str`, optional): Time period of the results
                ('day', 'week', 'month' or 'all_time').
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            state (:obj:`str`, optional): State of the question.
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        msg = "Must supply `album_id` or `song_id`."
        assert any([album_id, song_id]), msg
        msg = ("Pass only one of `album_id` and `song_id`"
               ", not both.")
        condition = (
            sum([bool(album_id), bool(song_id)])
            == 1
        )
        assert condition, msg
        endpoint = 'questions'
        params = {'per_page': per_page,
                  'page': page,
                  'state': state,
                  'text_format': text_format or self.response_format}
        if album_id:
            params['album_id'] = album_id
        elif song_id:
            params['song_id'] = song_id
        return self._make_request(path=endpoint, params_=params, public_api=True)
