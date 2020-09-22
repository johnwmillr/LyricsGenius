class VoterMethods(object):
    """Video methods of the public API."""

    def voters(self,
               annotation_id=None,
               answer_id=None,
               article_id=None,
               comment_id=None):
        """Gets the voters of an item.
        You must supply one of :obj:`annotation_id`, :obj:`answer_id`, :obj:`article_id`
        or :obj:`comment_id`.

        Args:
            annotation_id (:obj:`int`, optional): Genius annotation ID
            answer_id (:obj:`int`, optional): Genius answer ID
            article_id (:obj:`int`, optional): Genius article ID
            comment_id (:obj:`int`, optional): Genius comment ID

        Returns:
            :obj:`dict`

        """
        msg = "Must supply `annotation_id`, `answer_id`, `comment_id` or `article_id`"
        assert any([annotation_id, answer_id, article_id, comment_id]), msg
        msg = ("Pass only one of "
               "`annotation_id`, `answer_id`, `article_id` or `comment_id`"
               ", not more than one.")
        condition = (
            sum([bool(annotation_id),
                 bool(answer_id),
                 bool(article_id),
                 bool(comment_id)])
            == 1
        )
        assert condition, msg

        endpoint = 'voters'

        params = {}
        if annotation_id:
            params['annotation_id'] = annotation_id
        elif answer_id:
            params['answer_id'] = answer_id
        elif article_id:
            params['article_id'] = article_id
        elif comment_id:
            params['comment_id'] = comment_id
        return self._make_request(path=endpoint, params_=params)
