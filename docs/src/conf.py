import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'lyricsgenius'
copyright = '2025, John W. R. Miller, Allerter'
author = 'John W. R. Miller, Allerter'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
]

exclude_patterns = ['build']
master_doc = 'index'
autosummary_generate = True
# -- Options for HTML output -------------------------------------------------

highlight_language = 'python3'
html_theme = 'sphinx_rtd_theme'

# -- Other -------------------------------------------------------------------

extlinks = {
    'issue': ('https://github.com/johnwmillr/LyricsGenius/issues/%s', '%s'),
    'commit': ('https://github.com/johnwmillr/LyricsGenius/commit/%s', '%s')
}
