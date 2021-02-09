class LeaderboardMethods(object):
    """Leaderboard methods of the public API."""

    def leaderboard(self,
                    time_period='day',
                    per_page=None,
                    page=None,
                    text_format=None):
        """Gets the Genius community leaderboard.

        This method gets data of the community charts on the Genius.com page.

        Args:
            time_period (:obj:`str`, optional): Time period of the results.
                ('day', 'week', 'month' or 'all_time').
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        path = 'leaderboard'
        params = {'time_period': time_period,
                  'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=path, params_=params, public_api=True)

    def charts(self,
               time_period='day',
               chart_genre='all',
               per_page=None,
               page=None,
               text_format=None,
               type_='songs'):
        """Gets the Genius charts.

        This method gets data of the chart on the Genius.com page.

        Args:
            time_period (:obj:`str`, optional): Time period of the results.
                The default is `all`.
                ('day', 'week', 'month' or 'all_time').
            chart_genre (:obj:`str`, optional): The genre of the results.
                The default value is ``all``.
                ('all', 'rap', 'pop', 'rb', 'rock' or 'country')
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').
            type_ (:obj:`int`, optional): The type to get the charts for.
                The default is ``songs``.
                ('songs', 'albums', 'artists' or 'referents').

        Returns:
            :obj:`dict`

        .. Note::
            The *referents* mentioned in the description of the :obj:`type_`
            argument is shown as *Lyrics* in the drop-down menu on Genius.com
            where you choose the *Type*.

        """
        endpoint = type_ + '/chart'
        params = {'time_period': time_period,
                  'chart_genre': chart_genre,
                  'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)
