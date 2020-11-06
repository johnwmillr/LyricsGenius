.. _setup:


Setup
=====
Before we start installing the package, we'll need to get an access token.

Authorization
-------------
First you’ll need to sign up for a (free) account
that authorizes access to `the Genius API`_. After signing up/
logging in to your account, head out to the API section on Genius
and `create a new API client`_. After creating your client, you can
generate an access token to use with the library. Genius provides
two kinds of tokens:

- **client access token**:
    Mostly LyricsGenius is used to get song lyrics and song
    info. And this is also what the client access tokens are used for. They
    don't need a user to authenticate their use (through OAuth2 or etc) and
    you can easily get yours by visiting the `API Clients`_ page and click
    on *Generate Access Token*. This will give you an access token, and
    now you're good to go.

- **user token**:
    These tokens can do what client access tokens do and
    more. Using these you can get information of the account you have
    authenticated, create web-pages and create, manage and up-vote
    annotations that are hosted on your website. These tokens are
    really useful if you use Genius's `Web Annotator`_ on your website.
    Otherwise you won't have much need for this. Read more about
    user tokens on Genius's `documentation`_. LyricsGenius has a
    :ref:`auth` class that provides some helpful methods to get
    authenticate the user and get an access token.

Installation
------------

``lyricsgenius`` requires Python 3.

Use ``pip`` to install the package from PyPI:

.. code:: bash

   pip install lyricsgenius

Or, install the latest version of the package from GitHub:

.. code:: bash

   pip install git+https://github.com/johnwmillr/LyricsGenius.git


Now that you have the library intalled, you can get started with using
the library. See the :ref:`usage` for examples.

.. _Web Annotator: https://genius.com/web-annotator
.. _the Genius API: http://genius.com/api-clients
.. _API Clients: https://genius.com/api-clients
.. _Web Annotator: https://genius.com/web-annotator
.. _documentation: https://docs.genius.com/#/authentication-h1
.. _create a new API client: https://genius.com/api-clients/new
.. _create an app: http://genius.com/api-clients
.. _OAuth2: https://lyricsgenius.readthedocs.io/en/latest/reference/auth.html#auth
