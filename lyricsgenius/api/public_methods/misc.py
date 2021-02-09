class MiscMethods(object):
    """Miscellaneous Methods"""

    def line_item(self, line_item_id, text_format=None):
        """Gets data for a specific line item.

        Args:
            line_item_id (:obj:`int`): Genius line item ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Warning:
            This method requires a logged in user and will raise
            ``NotImplementedError``.

        """
        raise NotImplementedError('This action requires a logged in user.')

        endpoint = 'line_items/{}'.format(line_item_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def page_data(self, album=None, song=None, artist=None):
        """Gets page data of an item.

        If you want the page data of a song, you must supply
        song and artist. But if you want the page data of an album,
        you only have to supply the album.

        Page data will return all possible values for the album/song and
        the lyrics in HTML format if the item is a song!
        Album page data will contian album info and tracks info as well.

        Args:
            album (:obj:`str`, optional): Album path
                (e.g. '/albums/Eminem/Music-to-be-murdered-by')
            song (:obj:`str`, optional): Song path
                (e.g. '/Sia-chandelier-lyrics')
            artist (:obj:`str`, optional): Artist slug. (e.g. 'Andy-shauf')

        Returns:
            :obj:`dict`

        Warning:
            Some albums/songs either don't have page data or
            their page data path can't be infered easily from
            the artist slug and their API path. So make sure to
            use this method with a try/except clause that catches
            404 errors. Check out the example below.


        Examples:
            Getting the lyrics of a song from its page data

            .. code:: python

                from lyricsgenius import Genius, PublicAPI
                from bs4 import BeautifulSoup
                from requests import HTTPError

                genius = Genius(token)
                public = PublicAPI()

                # We need the PublicAPI to get artist's slug
                artist = public.artist(1665)
                artist_slug = artist['artist']['slug']

                # The rest can be done using Genius
                song = genius.song(4558484)
                song_path = song['song']['path']

                try:
                    page_data = genius.page_data(artist=artist_slug, song=song_path)
                except HTTPError as e:
                    print("Couldn't find page data {}".format(e.status_code))
                    page_data = None

                if page_data is not None:
                    lyrics_html = page_data['page_data']['lyrics_data']['body']['html']
                    lyrics_text = BeautifulSoup(lyrics_html, 'html.parser').get_text()

        """
        assert any([album, song]), "You must pass either song or album."
        if song:
            assert all([song, artist]), "You must pass artist."

        if album:
            endpoint = 'page_data/album'
            page_type = 'albums'
            item_path = album.replace('/albums/', '')
        else:
            endpoint = 'page_data/song'
            page_type = 'songs'

            # item path becomes something like: Artist/Song
            item_path = song[1:].replace(artist + '-', artist + '/').replace('-lyrics', '')

        page_path = '/{page_type}/{item_path}'.format(page_type=page_type,
                                                      item_path=item_path)
        params = {'page_path': page_path}

        return self._make_request(endpoint, params_=params, public_api=True)

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
        return self._make_request(path=endpoint, params_=params, public_api=True)
