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

    | All methods of this class are available through the :class:`Genius` class.

    Args:
        client_access_token (:obj:`str`): API key provided by Genius.
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.

    Attributes:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.

    Returns:
        :class:`API`: An object of the `API` class.

    """

    def __init__(self, client_access_token,
                 response_format='plain', timeout=5, sleep_time=0.5):
        super().__init__(
            client_access_token=client_access_token,
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time
        )

    def song(self, song_id, text_format=None):
        """Gets data for a specific song.

        Args:
            song_id (:obj:`int`): Genius song ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: Song details from Genius.

        Examples:
            .. code:: python

                genius = Genius(token)
                song = genius.song(2857381)
                print(song['full_title'])

        Note:
            This pure API method is used for fetching songs when you have their ID,
            and only makes a request to the API, therefore provides no lyrics.
            If you want the lyrics as well, use :meth:`Genius.search_song` instead.

        """
        endpoint = "songs/{id}".format(id=song_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(endpoint, params_=params)

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
                Either based on 'title' or 'popularity'.
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
        endpoint = "referents?"
        params = {'song_id': song_id, 'web_page_id': web_page_id,
                  'created_by_id': created_by_id,
                  'per_page': per_page, 'page': page,
                  'text_format': text_format or self.response_format}
        return self._make_request(endpoint, params_=params)

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

    | All methods of this class are available through the :class:`Genius` class.

    Args:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.

    Attributes:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.

    Returns:
        :class:`PublicAPI`: An object of the `PublicAPI` class.

    """

    def __init__(
        self,
        response_format='plain',
        timeout=5,
        sleep_time=0.5,
        **kwargs
    ):
        # Genius PublicAPI Constructor
        super().__init__(
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time,
            **kwargs
        )
