class VideoMethods(object):
    """Video methods of the public API."""

    def video(self, video_id, text_format=None):
        """Gets data for a specific video.

        Args:
            video_id (:obj:`int`): Genius video ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'videos/{}'.format(video_id)
        params = {'text_format': text_format or self.response_format}

        return self._make_request(path=endpoint, params_=params, public_api=True)

    def videos(self,
               album_id=None,
               article_id=None,
               song_id=None,
               video_id=None,
               per_page=None,
               page=None,
               series=False):
        """Gets the videos of an album, article or song or the featured videos.

        Args:
            album_id (:obj:`int`, optional): Genius album ID
            article_id (:obj:`int`, optional): Genius article ID
            song_id (:obj:`int`, optional): Genius song ID
            video_id (:obj:`int`, optional): Genius video ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).
            series (:obj:`bool`, optional): If set to `True`, returns episodes
            of Genius original video series that the item has been mentioned in.

        Returns:
            :obj:`dict`

        Note:
            If you specify no album, article or song, the method will return
            a series of videos. In this case, if `series=True`, the results
            will be the videos in the *VIDEOS* section on the homepage. But
            if `series=False`, the method returns another set of videos that
            we are not sure what they are at the moment.

        """
        msg = ("Pass only one of `album_id`, `article_id`, `song_id` and `video_id`."
               ", not more than one.")
        condition = (
            sum([bool(album_id), bool(article_id), bool(song_id), bool(video_id)])
            == 1
        )
        assert condition, msg

        if series:
            endpoint = 'video_lists'
        else:
            endpoint = 'videos'

        params = {'per_page': per_page,
                  'page': page}

        if album_id:
            params['album_id'] = album_id
        elif article_id:
            params['article_id'] = article_id
        elif song_id:
            params['song_id'] = song_id
        elif video_id:
            params['video_id'] = video_id

        return self._make_request(path=endpoint, params_=params, public_api=True)
