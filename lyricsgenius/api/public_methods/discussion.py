class DiscussionMethods(object):
    """Discussion methods of the public API."""

    def discussion(self, disscussion_id, text_format=None):
        """Gets data for a specific discussion.

        Args:
            disscussion_id (:obj:`int`): Genius discussion ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'discussions/{}'.format(disscussion_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def discussion_replies(self,
                           disscussion_id,
                           per_page=None,
                           page=None,
                           text_format=None):
        """Gets the replies on a discussion.

        Args:
            disscussion_id (:obj:`int`): Genius discussion ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'discussions/{}/forum_posts'.format(disscussion_id)
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)
