from .base import Sender
from .public_methods import (
    AlbumMethods,
    AnnotationMethods,
    ArticleMethods,
    ArtistMethods,
    CoverArtMethods,
    DiscussionMethods,
    LeaderboardMethods,
    QuestionMethods,
    ReferentMethods,
    SearchMethods,
    SongMethods,
    UserMethods,
    VideoMethods,
    MiscMethods
)


class API(Sender):
    """Genius API.

    The :obj:`API` class is in charge of making all the requests
    to the developers' API (api.genius.com)
    Use the methods of this class if you already have information
    such as song ID to make direct requests to the API. Otherwise
    the :class:`Genius` class provides a friendlier front-end
    to search and retrieve data from Genius.com.

    All methods of this class are available through the :class:`Genius` class.

    Args:
        access_token (:obj:`str`): API key provided by Genius.
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

    Attributes:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

    Returns:
        :class:`API`: An object of the `API` class.

    """

    def __init__(self,
                 access_token,
                 response_format='plain',
                 timeout=5,
                 sleep_time=0.2,
                 retries=0,
                 ):
        super().__init__(
            access_token=access_token,
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time,
            retries=retries,
        )

    def account(self, text_format=None):
        """Gets details about the current user.

        Requires scope: :obj:`me`.

        Args:
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = 'account'
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params)

    def annotation(self, annotation_id, text_format=None):
        """Gets data for a specific annotation.

        Args:
            annotation_id (:obj:`int`): annotation ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        params = {'text_format': text_format or self.response_format}
        endpoint = "annotations/{id}".format(id=annotation_id)
        return self._make_request(endpoint, params_=params)

    def create_annotation(self, text, raw_annotatable_url, fragment,
                          before_html=None, after_html=None,
                          canonical_url=None, og_url=None, title=None,
                          text_format=None):
        """Creates an annotation for a web page.

        Requires scope: :obj:`create_annotation`.

        Args:
            text (:obj:`str`): Annotation text in Markdown format.
            raw_annotatable_url (:obj:`str`): The original URL of the page.
            fragment (:obj:`str`): The highlighted fragment (the referent).
            before_html (:obj:`str`, optional): The HTML before the highlighted fragment
                (prefer up to 200 characters).
            after_html (:obj:`str`, optional): The HTML after the highlighted fragment
                (prefer up to 200 characters).
            canonical_url (:obj:`str`, optional): The href property of the
                :obj:`<link rel="canonical">` tag on the page.
            og_url (:obj:`str`, optional): The content property of the
                :obj:`<meta property="og:url">` tag on the page.
            title (:obj:`str`, optional): The title of the page.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        Examples:
            .. code:: python

                genius = Genius(token)
                new = genius.update_annotation('The annotation',
                'https://example.com', 'illustrative examples', title='test')
                print(new['id'])

        """
        msg = "Must supply `canonical_url`, `og_url`, or `title`."
        assert any([canonical_url, og_url, title]), msg

        endpoint = 'annotations'
        params = {'text_format': text_format or self.response_format}
        payload = {
            'annotation': {
                'body': {'markdown': text}
            },
            'referent': {
                'raw_annotatable_url': raw_annotatable_url,
                'fragment': fragment,
                'context_for_display': {
                    'before_html': before_html if before_html else None,
                    'after_html': after_html if after_html else None
                }
            },
            'web_page': {
                'canonical_url': canonical_url if canonical_url else None,
                'og_url': og_url if og_url else None,
                'title': title if title else None
            }
        }
        return self._make_request(path=endpoint, method='POST',
                                  params_=params, json=payload)

    def delete_annotation(self, annotation_id):
        """Deletes an annotation created by the authenticated user.

        Requires scope: :obj:`manage_annotation`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.

        Returns:
            :obj:`int`: 204 - which is the response's status code

        """
        endpoint = 'annotations/{}'.format(annotation_id)
        return self._make_request(path=endpoint, method='DELETE')

    def downvote_annotation(self, annotation_id, text_format=None):
        """Downvotes an annotation.

        Requires scope: :obj:`vote`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        endpoint = 'annotations/{}/downvote'.format(annotation_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, method='PUT', params_=params)

    def unvote_annotation(self, annotation_id, text_format=None):
        """Removes user's vote for the annotation.

        Requires scope: :obj:`vote`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        endpoint = 'annotations/{}/unvote'.format(annotation_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, method='PUT', params_=params)

    def update_annotation(self, annotation_id, text, raw_annotatable_url, fragment,
                          before_html=None, after_html=None,
                          canonical_url=None, og_url=None, title=None,
                          text_format=None):
        """Updates an annotation created by the authenticated user.

        Requires scope: :obj:`manage_annotation`.

        Args:
            annotation_id (:obj:`int`): ID of the annotation that will be updated.
            text (:obj:`str`): Annotation text in Markdown format.
            raw_annotatable_url (:obj:`str`): The original URL of the page.
            fragment (:obj:`str`): The highlighted fragment (the referent).
            before_html (:obj:`str`, optional): The HTML before the highlighted fragment
                (prefer up to 200 characters).
            after_html (:obj:`str`, optional): The HTML after the highlighted fragment
                (prefer up to 200 characters).
            canonical_url (:obj:`str`, optional): The href property of the
                :obj:`<link rel="canonical">` tag on the page.
            og_url (:obj:`str`, optional): The content property of the
                :obj:`<meta property="og:url">` tag on the page.
            title (:obj:`str`, optional): The title of the page.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        msg = "Must supply `canonical_url`, `og_url`, or `title`."
        assert any([canonical_url, og_url, title]), msg

        endpoint = 'annotations/{}'.format(annotation_id)
        params = {'text_format': text_format or self.response_format}
        payload = {
            'annotation': {
                'body': {'markdown': text}
            },
            'referent': {
                'raw_annotatable_url': raw_annotatable_url,
                'fragment': fragment,
                'context_for_display': {
                    'before_html': before_html if before_html else None,
                    'after_html': after_html if after_html else None
                }
            },
            'web_page': {
                'canonical_url': canonical_url if canonical_url else None,
                'og_url': og_url if og_url else None,
                'title': title if title else None
            }
        }
        return self._make_request(path=endpoint, method='PUT',
                                  params_=params, json=payload)

    def upvote_annotation(self, annotation_id, text_format=None):
        """Upvotes an annotation.

        Requires scope: :obj:`vote`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        endpoint = 'annotations/{}/upvote'.format(annotation_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, method='PUT', params_=params)

    def artist(self, artist_id, text_format=None):
        """Gets data for a specific artist.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                genius = Genius(token)
                artist = genius.artist(380491)
                print(artist['name'])

        """
        params = {'text_format': text_format or self.response_format}
        endpoint = "artists/{id}".format(id=artist_id)
        return self._make_request(endpoint, params_=params)

    def artist_songs(self, artist_id, per_page=None, page=None, sort='title'):
        """Gets artist's songs.

        Args:
            artist_id (:obj:`int`): Genius artist ID
            sort (:obj:`str`, optional): Sorting preference.
                Either based on 'title', 'popularity' or 'release_date'.
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                # getting all artist songs based on popularity
                genius = Genius(token)
                page = 1
                songs = []
                while page:
                    request = genius.artist_songs(380491,
                                                  sort='popularity',
                                                  per_page=50,
                                                  page=page)
                songs.extend(request['songs'])
                page = request['next_page']
                least_popular_song = songs[-1]['title']


                # getting songs 11-15
                songs = genius.artist_songs(380491, per_page=5, page=3)

        """
        endpoint = "artists/{id}/songs".format(id=artist_id)

        params = {'sort': sort,
                  'per_page': per_page,
                  'page': page}
        return self._make_request(endpoint, params_=params)

    def referents(self, song_id=None, web_page_id=None,
                  created_by_id=None, per_page=None, page=None, text_format=None):
        """Gets item's referents

        Args:
            song_id (:obj:`int`, optional): song ID
            web_page_id (:obj:`int`, optional): web page ID
            created_by_id (:obj:`int`, optional): User ID of the contributer
                who created the annotation(s).
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 50.
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Note:
            You may pass only one of :obj:`song_id` and
            :obj:`web_page_id`, not both.

        Examples:
            .. code:: python

                # getting all verified annotations of a song (artist annotations)
                genius = Genius(token)
                request = genius.referents(song_id=235729,
                                           per_page=50)
                verified = [y for x in request['referents']
                            for y in x['annotations'] if y['verified']]

        """
        msg = "Must supply `song_id`, `web_page_id`, or `created_by_id`."
        assert any([song_id, web_page_id, created_by_id]), msg
        msg = "Pass only one of `song_id` and `web_page_id`, not both."
        assert bool(song_id) ^ bool(web_page_id), msg

        # Construct the URI
        endpoint = "referents"
        params = {'text_format': text_format or self.response_format}
        params = {'song_id': song_id, 'web_page_id': web_page_id,
                  'created_by_id': created_by_id,
                  'per_page': per_page, 'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(endpoint, params_=params)

    def search_songs(self, search_term, per_page=None, page=None):
        """Searches songs hosted on Genius.

        Args:
            search_term (:obj:`str`): A term to search on Genius.
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 5 for this method.
            page (:obj:`int`, optional): Number of the page.

        Returns:
            :obj:`dict`

        """
        endpoint = "search"
        params = {'q': search_term,
                  'per_page': per_page,
                  'page': page}
        return self._make_request(endpoint, params_=params)

    def song(self, song_id, text_format=None):
        """Gets data for a specific song.

        Args:
            song_id (:obj:`int`): Genius song ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                genius = Genius(token)
                song = genius.song(2857381)
                print(song['full_title'])

        """
        endpoint = "songs/{id}".format(id=song_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(endpoint, params_=params)

    def web_page(self, raw_annotatable_url=None, canonical_url=None, og_url=None):
        """Gets data for a specific web page.

        Args:
            raw_annotatable_url (:obj:`str`): The URL as it would appear in a browser.
            canonical_url (:obj:`str`): The URL as specified by an appropriate <link>
                tag in a page's <head>.
            og_url (:obj:`str`): The URL as specified by an og:url <meta> tag in
                a page's <head>.

        Returns:
            :obj:`dict`

        Examples:
            .. code:: python

                genius = Genius(token)
                webpage = genius.web_page('docs.genius.com')
                print(webpage['full_title'])

        Note:
            * Data is only available for pages that already have at
              least one annotation.
            * You must at least pass one argument to the method.
            * You can pass more than one or all arguments (provided they're the address
              of the same webpage).

        """
        msg = "Must supply `raw_annotatable_url`, `canonical_url`, or `og_url`."
        assert any([raw_annotatable_url, canonical_url, og_url]), msg

        endpoint = 'web_pages/lookup'
        params = {'raw_annotatable_url': raw_annotatable_url,
                  'canonical_url': canonical_url,
                  'og_url': og_url}
        return self._make_request(path=endpoint, params_=params)


class PublicAPI(
        Sender,
        AlbumMethods,
        AnnotationMethods,
        ArticleMethods,
        ArtistMethods,
        CoverArtMethods,
        DiscussionMethods,
        LeaderboardMethods,
        QuestionMethods,
        ReferentMethods,
        SearchMethods,
        SongMethods,
        UserMethods,
        VideoMethods,
        MiscMethods):
    """Genius public API.

    The :obj:`PublicAPI` class is in charge of making all the requests
    to the public API (genius.com/api)
    You can use this method without an access token since calls are made
    to the public API.

    All methods of this class are available through the :class:`Genius` class.

    Args:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

    Attributes:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

    Returns:
        :class:`PublicAPI`: An object of the `PublicAPI` class.

    """

    def __init__(
        self,
        response_format='plain',
        timeout=5,
        sleep_time=0.2,
        retries=0,
        **kwargs
    ):

        # If PublicAPI was instantiated directly
        # there is no need for a token anymore
        public_api_constructor = False if self.__class__.__name__ == 'Genius' else True

        # Genius PublicAPI Constructor
        super().__init__(
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time,
            retries=retries,
            public_api_constructor=public_api_constructor,
            **kwargs
        )
