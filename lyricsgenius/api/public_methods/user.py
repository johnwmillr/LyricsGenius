class UserMethods(object):
    """User methods of the public API."""

    def user(self, user_id, text_format=None):
        """Gets data for a specific user.

        Args:
            user_id (:obj:`int`): Genius user ID
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        path = 'users/{}'.format(user_id)
        params = {'text_format': text_format or self.response_format}
        return self._make_request(path, params_=params, public_api=True)

    def user_accomplishments(self,
                             user_id,
                             per_page=None,
                             next_cursor=None,):
        """Gets user's accomplishments.

        This methods gets the section titled "TOP ACCOMPLISHMENTS" in
        the user's profile.

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).

        Returns:
            :obj:`dict`

        """
        endpoint = 'users/{}/accomplishments'.format(user_id)
        params = {'next_cursor': next_cursor,
                  'per_page': per_page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def user_following(self,
                       user_id,
                       per_page=None,
                       page=None):
        """Gets the accounts user follows.

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """
        endpoint = 'users/{}/followed_users'.format(user_id)
        params = {'page': page,
                  'per_page': per_page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def user_followers(self,
                       user_id,
                       per_page=None,
                       page=None):
        """Gets user's followers.

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            page (:obj:`int`, optional): Paginated offset (number of the page).

        Returns:
            :obj:`dict`

        """
        endpoint = 'users/{}/followers'.format(user_id)
        params = {'page': page,
                  'per_page': per_page}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def user_contributions(self,
                           user_id,
                           per_page=None,
                           next_cursor=None,
                           sort=None,
                           text_format=None,
                           type_=None):
        """Gets user's contributions.

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').
            type_ (:obj:`int`, optional): Type of the contribution
                ('annotations', 'articles', 'pyongs', 'questions_and_answers',
                'comments', 'transcriptions' or 'unreviewed annotations').

        Returns:
            :obj:`dict`


        Note:
            Not all types support a sorting preference. Setting the :obj:`sort` for
            these types won't result in erros, but won't make a difference in the
            results either. To find out which types support which features, look at
            the alias methods.

        Note:
            Setting no value for the :obj:`type_` will return the user's contributions
            (regardless of its type) in chronological order; just like visting a
            user's profile page and scrolling down, looking at their contributions over
            time.

        """
        endpoint = 'users/{}/contributions'.format(user_id)
        if type_ is not None:
            endpoint += '/{}'.format(type_)
        params = {'next_cursor': next_cursor,
                  'per_page': per_page,
                  'sort': sort,
                  'text_format': text_format or self.response_format}
        return self._make_request(path=endpoint, params_=params, public_api=True)

    def user_annotations(self,
                         user_id,
                         per_page=None,
                         next_cursor=None,
                         sort='popularity',
                         text_format=None
                         ):
        """Gets user's annotations.

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            sort=sort,
            text_format=text_format,
            type_='annotations'
        )

    def user_articles(self,
                      user_id,
                      per_page=None,
                      next_cursor=None,
                      sort='popularity',
                      text_format=None
                      ):
        """Gets user's articles.

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            sort=sort,
            text_format=text_format,
            type_='articles'
        )

    def user_pyongs(self,
                    user_id,
                    per_page=None,
                    next_cursor=None,
                    text_format=None):
        """Gets user's Pyongs.

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            text_format=text_format,
            type_='pyongs'
        )

    def user_questions_and_answers(self,
                                   user_id,
                                   per_page=None,
                                   next_cursor=None,
                                   text_format=None):
        """Gets user's Q&As.

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            text_format=text_format,
            type_='questions_and_answers'
        )

    def user_suggestions(self,
                         user_id,
                         per_page=None,
                         next_cursor=None,
                         text_format=None):
        """Gets user's suggestions (comments).

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            text_format=text_format,
            type_='comments'
        )

    def user_transcriptions(self,
                            user_id,
                            per_page=None,
                            next_cursor=None,
                            sort='popularity',
                            text_format=None):
        """Gets user's transcriptions.

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            sort=sort,
            text_format=text_format,
            type_='transcriptions'
        )

    def user_unreviewed(self,
                        user_id,
                        per_page=None,
                        next_cursor=None,
                        sort='popularity',
                        text_format=None):
        """Gets user's unreviewed annotations.

        Alias for :meth:`user_contributions() <PublicAPI.user_contributions>`

        This method gets user annotations that have the
        "This annotations is unreviewed" sign above them.

        Args:
            user_id (:obj:`int`): Genius user ID
            per_page (:obj:`int`, optional): Number of results to
                return per request. It can't be more than 50.
            next_cursor (:obj:`str`, optional): Paginated offset
                (address of the next cursor).
            sort (:obj:`str`, optional): Sorting preference.
                ('title' or 'popularity')
            text_format (:obj:`str`, optional): Text format of the results
                ('dom', 'html', 'markdown' or 'plain').

        Returns:
            :obj:`dict`

        """
        return self.user_contributions(
            user_id=user_id,
            next_cursor=next_cursor,
            per_page=per_page,
            sort=sort,
            text_format=text_format,
            type_='unreviewed_annotations'
        )
