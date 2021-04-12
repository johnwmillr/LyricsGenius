Contributing
------------
If you'd like to contribute to LyricsGenius by fixing a bug,
introducing a new feature, improving the docs or whatever else,
you can follow the steps below:

- First, fork the repository.
- Clone your fork on your local machine. Then install the package
  in editable mode with developer dependencies. Either create a branch
  with an appropriate name for your change (recommended) or just use
  the ``master`` branch. This way you can easily run our tests.

  .. code:: bash

    git clone https://github.com/my-username/LyricsGenius
    cd LyricsGenius
    # If you want, you can check out a new branch. For example:
    # git branch my-new-feature
    # git checkout my-new-feature
    pip install -e .[dev]

- Now you can make the changes you intended.
- Before committing your changes, you can run our tests to make
  sure everything is working okay. If you have already committed
  the changes, no worries. Run the tests and then commit the fixes
  needed.
  There are three ways to run the tests:

  - ``tox -e test``: runs the unit tests (needs the following environment
    variables: ``GENIUST_ACCESS_TOKEN``, ``GENIUS_CLIENT_ID``,
    ``GENIUS_CLIENT_SECRET`` and ``GENIUS_REDIRECT_URI``). Note that you
    can skip these tests if your changes only affect the docs or you
    think setting up the unit tests are too much trouble.

  - ``tox -e lint``: runs linting tests for the code and the docs.
  - ``tox``: runs all tests (both of the ones above).
- After you're done, you can open a pull request and we'll review your changes.
  Thanks for contributing to LyricsGenius!
