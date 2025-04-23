from typing import Any, Literal

from ..types.types import TextFormatT
from .base import Sender
from .public_methods import (
    AlbumMethods,
    AnnotationMethods,
    ArticleMethods,
    ArtistMethods,
    CoverArtMethods,
    DiscussionMethods,
    LeaderboardMethods,
    MiscMethods,
    QuestionMethods,
    ReferentMethods,
    SearchMethods,
    SongMethods,
    UserMethods,
    VideoMethods,
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
        user_agent (:obj:`str`, optional): User agent for the request header.
        proxy (:obj:`dict[str, str]`, optional): Proxy settings.

    Attributes:
        response_format (:obj:`str`, optional): API response format (dom, plain, html).
        timeout (:obj:`int`, optional): time before quitting on response (seconds).
        sleep_time (:obj:`str`, optional): time to wait between requests.
        retries (:obj:`int`, optional): Number of retries in case of timeouts and
            errors with a >= 500 response code. By default, requests are only made once.

    Returns:
        :class:`API`: An object of the `API` class.

    """

    def __init__(
        self,
        access_token: str | None = None,
        response_format: Literal["dom", "plain", "html"] = "plain",
        timeout: int = 5,
        sleep_time: float = 0.2,
        retries: int = 0,
        user_agent: str = "",
        proxy: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            access_token=access_token,
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time,
            retries=retries,
            user_agent=user_agent,
            proxy=proxy,
        )

    def account(self, text_format: TextFormatT | None = None) -> dict[str, Any]:
        """Gets details about the current user.

        Requires scope: :obj:`me`.

        Args:
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        endpoint = "account"
        params = {"text_format": text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params)

    def annotation(
        self,
        annotation_id: int,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Gets data for a specific annotation.

        Args:
            annotation_id (:obj:`int`): annotation ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        params = {"text_format": text_format or self.response_format}
        endpoint = "annotations/{id}".format(id=annotation_id)
        return self._make_request(endpoint, params_=params)

    def create_annotation(
        self,
        text: str,
        raw_annotatable_url: str,
        fragment: str,
        before_html: str | None = None,
        after_html: str | None = None,
        canonical_url: str | None = None,
        og_url: str | None = None,
        title: str | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
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

        endpoint = "annotations"
        params = {"text_format": text_format or self.response_format}
        payload = {
            "annotation": {"body": {"markdown": text}},
            "referent": {
                "raw_annotatable_url": raw_annotatable_url,
                "fragment": fragment,
                "context_for_display": {
                    "before_html": before_html if before_html else None,
                    "after_html": after_html if after_html else None,
                },
            },
            "web_page": {
                "canonical_url": canonical_url if canonical_url else None,
                "og_url": og_url if og_url else None,
                "title": title if title else None,
            },
        }
        return self._make_request(
            path=endpoint, method="POST", params_=params, json=payload
        )

    def delete_annotation(self, annotation_id: int) -> int | None:
        """Deletes an annotation created by the authenticated user.

        Requires scope: :obj:`manage_annotation`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.

        Returns:
            :obj:`int`: 204 - which is the response's status code

        """
        return self._make_request(
            path=f"annotations/{annotation_id}", method="DELETE"
        ).get("status_code")

    def downvote_annotation(
        self,
        annotation_id: int,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Downvotes an annotation.

        Requires scope: :obj:`vote`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        return self._make_request(
            path=f"annotations/{annotation_id}/downvote",
            method="PUT",
            params_={"text_format": text_format or self.response_format},
        )

    def unvote_annotation(
        self,
        annotation_id: int,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Removes user's vote for the annotation.

        Requires scope: :obj:`vote`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        return self._make_request(
            path=f"annotations/{annotation_id}/unvote",
            method="PUT",
            params_={"text_format": text_format or self.response_format},
        )

    def update_annotation(
        self,
        annotation_id: int,
        text: str,
        raw_annotatable_url: str,
        fragment: str,
        before_html: str | None = None,
        after_html: str | None = None,
        canonical_url: str | None = None,
        og_url: str | None = None,
        title: str | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
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

        payload = {
            "annotation": {"body": {"markdown": text}},
            "referent": {
                "raw_annotatable_url": raw_annotatable_url,
                "fragment": fragment,
                "context_for_display": {
                    "before_html": before_html if before_html else None,
                    "after_html": after_html if after_html else None,
                },
            },
            "web_page": {
                "canonical_url": canonical_url if canonical_url else None,
                "og_url": og_url if og_url else None,
                "title": title if title else None,
            },
        }
        return self._make_request(
            path=f"annotations/{annotation_id}",
            method="PUT",
            params_={"text_format": text_format or self.response_format},
            json=payload,
        )

    def upvote_annotation(
        self,
        annotation_id: int,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Upvotes an annotation.

        Requires scope: :obj:`vote`.

        Args:
            annotation_id (:obj:`int`): Annotation ID.
            text_format (:obj:`str`, optional): Text format of the response
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`: The annotation.

        """
        return self._make_request(
            path=f"annotations/{annotation_id}/upvote",
            method="PUT",
            params_={"text_format": text_format or self.response_format},
        )

    def artist(
        self,
        artist_id: int,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
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
        return self._make_request(
            path=f"artists/{artist_id}",
            params_={"text_format": text_format or self.response_format},
        )

    def artist_songs(
        self,
        artist_id: int,
        per_page: int | None = None,
        page: int | None = None,
        sort: str = "title",
    ) -> dict[str, Any]:
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
        return self._make_request(
            path=f"artists/{artist_id}/songs",
            params_={"sort": sort, "per_page": per_page, "page": page},
        )

    def referents(
        self,
        song_id: int | None = None,
        web_page_id: int | None = None,
        created_by_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
        """Gets item's referents

        Args:
            song_id (:obj:`int`, optional): song ID
            web_page_id (:obj:`int`, optional): web page ID
            created_by_id (:obj:`int`, optional): User ID of the contributor
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
        params: dict[str, Any] = {"text_format": text_format or self.response_format}
        params = {
            "song_id": song_id,
            "web_page_id": web_page_id,
            "created_by_id": created_by_id,
            "per_page": per_page,
            "page": page,
            "text_format": text_format or self.response_format,
        }
        return self._make_request(path="referents", params_=params)

    def search_songs(
        self, search_term: str, per_page: int | None = None, page: int | None = None
    ) -> dict[str, Any]:
        """Searches songs hosted on Genius.

        Args:
            search_term (:obj:`str`): A term to search on Genius.
            per_page (:obj:`int`, optional): Number of results to
                return per page. It can't be more than 5 for this method.
            page (:obj:`int`, optional): Number of the page.

        Returns:
            :obj:`dict`

        """
        return self._make_request(
            path="search",
            params_={"q": search_term, "per_page": per_page, "page": page},
        )

    def song(
        self,
        song_id: int,
        text_format: TextFormatT | None = None,
    ) -> dict[str, Any]:
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
        return self._make_request(
            path=f"songs/{song_id}",
            params_={"text_format": text_format or self.response_format},
        )

    def web_page(
        self,
        raw_annotatable_url: str | None = None,
        canonical_url: str | None = None,
        og_url: str | None = None,
    ) -> dict[str, Any]:
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

        return self._make_request(
            path="web_pages/lookup",
            params_={
                "raw_annotatable_url": raw_annotatable_url,
                "canonical_url": canonical_url,
                "og_url": og_url,
            },
        )


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
    MiscMethods,
):
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
        response_format: Literal["dom", "plain", "html"] = "plain",
        timeout: int = 5,
        sleep_time: float = 0.2,
        retries: int = 0,
        user_agent: str = "",
        **kwargs: Any,
    ) -> None:
        # If PublicAPI was instantiated directly
        # there is no need for a token anymore
        public_api_constructor = False if self.__class__.__name__ == "Genius" else True

        # Genius PublicAPI Constructor
        super().__init__(
            response_format=response_format,
            timeout=timeout,
            sleep_time=sleep_time,
            retries=retries,
            public_api_constructor=public_api_constructor,
            user_agent=user_agent,
            **kwargs,
        )
