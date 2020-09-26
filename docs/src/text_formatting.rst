
Text Formatting
===============
Usually, when making calls to the API, there is a ``text_format`` parameter to
determine the text format of the text inside the response. LyricsGenius
provides a ``Genius.response_format`` that you can set and will be used for
all the calls that support a ``text_format`` parameter (not all endpoints have
a text body to return so the parameter would be pointless). Let's read what
Genius docs say about text formatting:

    Many API requests accept a text_format query parameter that can be used to
    specify how text content is formatted. The value for the parameter must be
    one or more of plain, html, and dom. The value returned will be an object
    with key-value pairs of formats and results:

    * **plain** is just plain text, no markup
    * **html** is a string of unescaped HTML suitable for rendering by a
      browser
    * **dom** is a nested object representing and HTML DOM hierarchy that
      can be used to programmatically present structured content


Now what Genius hasn't documented is that there is one more format except the
three ones above and that you can use more that one at a time. The other format
is the ``markdown`` format that returns results in the Markdown format.
Besides the four available formats, you can get more than one format in a call.
To do this you simply set the ``Genius.response_format`` like this:

.. code:: python

    genius.response_format = 'plain,html'

Doing this will return the ``plain`` and ``html`` formats in the body of the
results. Let's give it a try:

.. code:: python

    import lyricsgenius
    genius = lyricsgenius.Genius('token') # you can also set the attribute here
    genius.response_format = 'plain,html'

    res = genius.annotation(10225840)

    # Annotation in plain formatting
    print(res['annotation']['body']['plain'])

    # Annotation in html formatting
    print(res['annotation']['body']['html'])

You can also specify the text formatting in the call:

.. code:: python

    genius.annotation(10225840, text_format='html')

Using this will override ``response_format`` for this specific call.
If you pass no ``text_format``, the formatting will default to
the ``response_format`` attribute if the method supports text formatting.


Available Formats
-----------------
* **plain** is just plain text, no markup
* **html** is a string of unescaped HTML suitable for rendering by a browser
* **dom** is a nested object representing an HTML DOM hierarchy that can be
  used to programmatically present structured content
* **markdown** is text with Markdown formatting
