Contributing
------------
Please contribute! Genius has a lot of undocumented API endpoints.
You could try to look through Genius yourself to uncover new ones, and
implement them. Or you could go through the only ones that have already
been implemented and try to make more sense of the parameters they take.

If you want to fix a bug, suggest improvements, or
add new features to the project, just `open an issue`_ on GitHub.

If you want to run the checks on your machine before opening a
PR, install `uv`_ and do the following:

.. code:: bash

    cd LyricsGenius
    uv sync

This installs the package in development mode with everything needed to
check your changes:

- ``uv run pytest``: runs the unit tests.
- ``uv run ruff check`` and ``uv run ruff format``: lint and format the code.
- ``uv run mypy``: type checks the package.

Running ``uv run pre-commit install`` once runs all of these on every commit.

The tests never reach the network. Tests of API methods replay responses
recorded in ``tests/cassettes``. If you add one, set ``GENIUS_ACCESS_TOKEN``
and run ``uv run pytest --record-mode=once`` to record its cassette; the token
is not saved in it. Tests marked ``live`` make real requests and only run with
``uv run pytest --live``.


Releasing
*********
Releases are driven entirely by tags. The package version is derived from the
tag by ``hatch-vcs``, so there is no version to bump anywhere in the tree.

To cut a release, tag a commit on ``master`` and push the tag:

.. code:: bash

    git tag v3.15.0
    git push origin v3.15.0

Pushing a ``v*`` tag runs the ``publish`` workflow, which builds the package,
uploads it to PyPI, and creates the matching GitHub release with the built
artifacts attached. A run that fails partway can simply be re-run; nothing
needs to change in the repository first.


.. _open an issue: https://github.com/johnwmillr/LyricsGenius/issues
.. _uv: https://docs.astral.sh/uv/
