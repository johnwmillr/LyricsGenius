# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import sys
import re
from os import path
from setuptools import find_packages, setup

assert sys.version_info[0] == 3, "LyricsGenius requires Python 3."

VERSIONFILE = "lyricsgenius/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError(
        "Unable to find version string in {}".format(VERSIONFILE))

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

extras_require = {
    'docs': [
        'sphinx~=3.3',
        'sphinx-rtd-theme',
    ],
    'checks': [
        'tox~=3.2',
        'doc8',
        'flake8',
        'flake8-bugbear',
        'pygments',
    ]
}
extras_require['dev'] = (
    extras_require['docs'] + extras_require['checks']
)

setup(
    name='lyricsgenius',
    version=version,
    description='Download lyrics and metadata from Genius.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    author='John W. Miller',
    author_email='john.w.millr+lg@gmail.com',
    url='https://github.com/johnwmillr/lyricsgenius',
    keywords='genius api genius-api music lyrics artists albums songs',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'beautifulsoup4>=4.6.0',
        'requests>=2.20.0'
    ],
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'lyricsgenius = lyricsgenius.__main__:main']
    },
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
