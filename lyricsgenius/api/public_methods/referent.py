class ReferentMethods(object):
    """Referent methods of the public API."""

    def referent(self, referent_ids, text_format=None):
        """Gets data of one or more referents.
        This method can get multiple referents in one call,
        thus increasing performance.

        Args:
            referent_ids (:obj:`list`): A list of referent IDs.
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Note:
            Using this method you can get the referent itself instead of
            the referents of a song or webpage which is what
            :meth:`referents() <PublicAPI.referents>` gets.

        """
        params = {'text_format': text_format or self.response_format}
        if len(referent_ids) == 1:
            endpoint = 'referents/{}'.format(referent_ids[0])
        else:
            endpoint = 'referents/multi'
            params = [('text_format', params['text_format'])]
            for id in referent_ids:
                params.append(('ids[]', id))

        return self._make_request(path=endpoint, params_=params, public_api=True)

    def referents(self, song_id=None, web_page_id=None,
                  created_by_id=None, per_page=None, page=None, text_format=None):
        """Gets item's referents

        You must supply :obj:`song_id`, :obj:`web_page_id`, or :obj:`created_by_id`.

        Args:
            song_id (:obj:`int`, optional): song ID
            web_page_id (:obj:`int`, optional): web page ID
            created_by_id (:obj:`int`, optional): User ID of the contributer
                who created the annotation(s).
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 50.
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        msg = "Must supply `song_id`, `web_page_id`, or `created_by_id`."
        assert any([song_id, web_page_id, created_by_id]), msg
        msg = "Pass only one of `song_id` and `web_page_id`, not both."
        assert bool(song_id) ^ bool(web_page_id), msg

        endpoint = "referents"
        params = {'song_id': song_id,
                  'web_page_id': web_page_id,
                  'created_by_id': created_by_id,
                  'per_page': per_page, 'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(endpoint, params_=params, public_api=True)

    def referents_charts(self,
                         time_period='day',
                         chart_genre='all',
                         per_page=None,
                         page=None,
                         text_format=None):
        """Gets the referents (lyrics) charts.

        Alias for :meth:`charts() <PublicAPI.charts>`.

        Args:
            time_period (:obj:`str`, optional): Time period of the results
                ('day', 'week', 'month' or 'all_time').
            chart_genre (:obj:`str`, optional): The genre of the results.
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.charts(
            time_period=time_period,
            chart_genre=chart_genre,
            per_page=per_page,
            page=page,
            text_format=text_format,
            type_='referents'
        )
