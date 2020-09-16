Contributing
------------
Please contribute! Genius has a lot of `undocumented API endpoints`_, and
the ones in that link are only some of them. You could try to implement the
ones in the link or look through Genius yourself to uncover new ones, and
implement them in LyricsGenius to make this client richer in features, and
the access it offers to Genius.com.

If you want to fix a bug, suggest improvements, or
add new features to the project, just `open an issue`_ on GitHub.

LyricsGenius coheres to a certain set of rules for the style of the code
in the package and its documentation. To make sure your changes are
following these styling guidelines, first, install the package in editable
mode using:

.. code:: bash

    git clone https://github.com/johnwmillr/LyricsGenius.git
    cd lyricsgenius
    pip install -e .[dev]


This installs the package along with the packages you need for testing
your code (you can also do it manually by installing the packages listed
in `setup.py`).
After you have made your changes, you can easily check them:

.. code:: bash

    cd lyricsgenius
    tox -e lint


If there are any issues in your changes, `tox` will point them out
for you. If you face any problems fixing those issues, just open
your PR and we'll help!


.. _open an issue: https://github.com/johnwmillr/LyricsGenius/issues
.. _undocumented API endpoints: https://github.com/shaedrich/
    geniusly/wiki/Undocumented-API-endpoints
