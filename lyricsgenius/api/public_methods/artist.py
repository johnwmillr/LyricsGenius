class ArtistMethods(object):
    """Artist methods of the public API."""

    def artist(self, artist_id, text_format=None):
        """Gets data for a specific artist.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}'.format(artist_id)
        params = {'text_format': text_format or self.response_format}

        return self._make_request(path=endpoint, params_=params, public_api=True)

    def artist_activity(self, artist_id, per_page=None, page=None, text_format=None):
        """Gets activities on artist's songs.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}/activity_stream/line_items'.format(artist_id)
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def artist_albums(self, artist_id, per_page=None, page=None):
        """Gets artist's albums.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}/albums'.format(artist_id)
        params = {'per_page': per_page,
                  'page': page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def artist_contribution_opportunities(self,
                                          artist_id,
                                          per_page=None,
                                          next_curosr=None,
                                          text_format=None):
        """Gets contribution opportunities related to the artist.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`int`, optional): Paginated offset
                (address of the next cursor).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Warning:
            This method requires a logged in user and will raise
            ``NotImplementedError``.

        """
        raise NotImplementedError('This action requires a logged in user.')
        endpoint = 'artists/{}/contribution_opportunities'.format(artist_id)
        params = {'per_page': per_page,
                  'next_curosr': next_curosr,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def artist_followers(self, artist_id, per_page=None, page=None):
        """Gets artist's followers.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}/followers'.format(artist_id)
        params = {'per_page': per_page,
                  'page': page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def artist_leaderboard(self, artist_id, per_page=None, page=None):
        """Gets artist's top scholars.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}/leaderboard'.format(artist_id)
        params = {'per_page': per_page,
                  'page': page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def artist_songs(self, artist_id, per_page=None, page=None, sort='popularity'):
        """Gets artist's songs.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}/songs'.format(artist_id)
        params = {'per_page': per_page,
                  'page': page,
                  'sort': sort}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def search_artist_songs(self,
                            artist_id,
                            search_term,
                            per_page=None,
                            page=None,
                            sort='popularity'):
        """Searches artist's songs.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            search_term (:obj:`str`): A term to search on Genius.
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')

        Returns:
            :obj:`dict`

        """
        endpoint = 'artists/{}/songs/search'.format(artist_id)
        params = {'q': search_term,
                  'per_page': per_page,
                  'page': page,
                  'sort': sort}
        return self._make_request(path=endpoint, params_=params, public_api=True)
