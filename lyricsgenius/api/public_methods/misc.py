class MiscMethods:
    """Miscellaneous Methods"""

    def line_item(self, line_item_id, text_format=None):
        """Gets data for a specific song.

        Args:
            line_item_id (:obj:`int`): Genius line item ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'line_items/{}'.format(line_item_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)
