class SearchMethods(object):
    """Search methods of the public API."""

    def search(self, search_term, per_page=None, page=None, type_=''):
        """Searches Genius.

        Args:
            search_term (:obj:`str`): A term to search on Genius.
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').
            type_ (:obj:`str`, optional): Type of item to search for
                ('song', 'lyric', 'artist', 'album', 'video',
                'article', 'user' or 'multi').

        Returns:
            :obj:`dict`

        .. Note::
            Specifying no :obj:`type_` parameter (which defaults to ``''``) or
            setting it as ``song`` will return the same results. Both will return
            songs. The only different is they return the hits in different
            keys:

                * ``type_=''``: ``response['hits']``
                * ``type_='song'``: ``response['sections'][0]['hits']``

            By Setting the type as ``multi`` the method will perform a search
            for all the other types and return an extra section called ``top hits``.

        .. Note::
            Instead of calling this method directly and specifying a type, you
            can use the alias methods.

        """
        if type_ == '':
            path = 'search'
        else:
            path = 'search/' + type_
        params = {'q': search_term,
                  'per_page': per_page,
                  'page': page}
        return self._make_request(path, params_=params, public_api=True)

    def search_albums(self, search_term, per_page=None, page=None):
        """Searches the albums on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'album'
        return self.search(search_term, per_page, page, endpoint)

    def search_articles(self, search_term, per_page=None, page=None):
        """Searches the articles on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'article'
        return self.search(search_term, per_page, page, endpoint)

    def search_artists(self, search_term, per_page=None, page=None):
        """Searches the artists on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'artist'
        return self.search(search_term, per_page, page, endpoint)

    def search_lyrics(self, search_term, per_page=None, page=None):
        """Searches the lyrics on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'lyric'
        return self.search(search_term, per_page, page, endpoint)

    def search_songs(self, search_term, per_page=None, page=None):
        """Searches the songs on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'song'
        return self.search(search_term, per_page, page, endpoint)

    def search_users(self, search_term, per_page=None, page=None):
        """Searches the users on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'user'
        return self.search(search_term, per_page, page, endpoint)

    def search_videos(self, search_term, per_page=None, page=None):
        """Searches the videos on Genius.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'video'
        return self.search(search_term, per_page, page, endpoint)

    def search_all(self, search_term, per_page=None, page=None):
        """Searches all types.

        Including: albums, articles, lyrics, songs, users and
        videos.

        Alias for :meth:`search() <PublicAPI.search>`

        Args:
            search_term (:obj:`str`): A term to search on Genius.
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 5 for this method.
            page (:obj:`int`, optional): Number of the page.

        Returns:
            :obj:`dict`

        Note:
            This method will also return a ``top hits`` section
            alongside other types.

        """
        endpoint = 'multi'
        return self.search(search_term, per_page, page, endpoint)
