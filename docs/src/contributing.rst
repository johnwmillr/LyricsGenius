Contributing
------------
Please contribute! Genius has a lot of undocumented API endpoints.
You could try to look through Genius yourself to uncover new ones, and
implement them. Or you could go through the only ones that have already
been implemented and try to make more sense of the parameters they take.

If you want to fix a bug, suggest improvements, or
add new features to the project, just `open an issue`_ on GitHub.

If you want to run the tests on your machine before opening a
PR, do the following: 

.. code:: bash

    cd LyricsGenius
    pip install -e .[dev]

This will install the package in developer mode with all the packages
necessary for running the tests. Now you can run three types of commands
to test your changes:

- ``tox -e test``: runs the unit tests.
- ``tox -e lint``: runs flake8 (PEP8 for code), doc8 (PEP8 for docs)
  and tests creating docs.
- ``tox``: runs all tests (both of the ones above).



.. _open an issue: https://github.com/johnwmillr/LyricsGenius/issues
