class AnnotationMethods(object):
    """Annotation methods of the public API."""

    def annotation(self, annotation_id, text_format=None):
        """Gets data for a specific annotation.

        Args:
            annotation_id (:obj:`int`): Genius annotation ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'annotations/{}'.format(annotation_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def annotation_edits(self, annotation_id, text_format=None):
        """Gets the edits on annotation (its versions).

        Args:
            annotation_id (:obj:`int`): Genius annotation ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'annotations/{}/versions'.format(annotation_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def annotation_comments(self,
                            annotation_id,
                            per_page=None,
                            page=None,
                            text_format=None):
        """Gets the comments on an annotation.

        Args:
            annotation_id (:obj:`int`): Genius annotation ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'annotations/{}/comments'.format(annotation_id)
        params = {'per_page': per_page,
                  'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)
