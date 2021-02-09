class ArticleMethods(object):
    """Article methods of the public API."""

    def article(self, article_id, text_format=None):
        """Gets data for a specific article.

        Args:
            article_id (:obj:`int`): Genius article ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'articles/{}'.format(article_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def article_comments(self, article_id, per_page=None, page=None, text_format=None):
        """Gets the comments on an article.

        Args:
            article_id (:obj:`int`): Genius article ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'articles/{}/comments'.format(article_id)
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def latest_articles(self, per_page=None, page=None, text_format=None):
        """Gets the latest articles on the homepage.

        This method will return the featured articles that are placed
        on top of the Genius.com page.

        Args:
            article_id (:obj:`int`): Genius article ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'editorial_placements/latest'
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)
