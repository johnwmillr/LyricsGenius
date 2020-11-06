class AlbumMethods(object):
    """Album methods of the public API."""

    def album(self, album_id, text_format=None):
        """Gets data for a specific album.

        Args:
            album_id (:obj:`int`): Genius album ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                genius = Genius(token)
                song = genius.search_song(378195)
                album_id = song['album']['id']
                album = genius.album(album_id)
                print(album['name'])

        """
        endpoint = 'albums/{}'.format(album_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def albums_charts(self,
                      time_period='day',
                      chart_genre='all',
                      per_page=None,
                      page=None,
                      text_format=None):
        """Gets the album charts.

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
            type_='albums'
        )

    def album_comments(self, album_id, per_page=None, page=None, text_format=None):
        """Gets the comments on an album page.

        Args:
            album_id (:obj:`int`): Genius album ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'albums/{}/comments'.format(album_id)
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def album_cover_arts(self, album_id, text_format=None):
        """Gets cover arts of a specific album.

        Alias for :meth:`cover_arts <PublicAPI.cover_arts>`.

        Args:
            album_id (:obj:`int`): Genius album ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain'). Defines the text
                formatting for the annotation of the cover arts,
                if there are any.

        Returns:
            :obj:`dict`

        Examples:
            Downloading album's cover art:

            .. code:: python

                import requests

                genius = Genius(token)
                res = genius.album_cover_arts(104614)
                cover_art = requests.get(res['cover_arts'][0]['image_url'])

        """
        return self.cover_arts(album_id=album_id, text_format=text_format)

    def album_leaderboard(self, album_id, per_page=None, page=None):
        """Gets the leaderboard of an album.

        This method returns the album's top contributors.

        Args:
            album_id (:obj:`int`): Genius album ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """
        endpoint = 'albums/{}/leaderboard'.format(album_id)
        params = {'per_page': per_page,
                  'page': page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def album_tracks(self, album_id, per_page=None, page=None, text_format=None):
        """Gets the tracks of a specific album.

        Args:
            album_id (:obj:`int`): Genius album ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'albums/{}/tracks'.format(album_id)
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)
