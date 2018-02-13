import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='geniuslyrics',
    version='0.0',
    description='GeniusLyrics',
    long_description=README,
    classifiers=[
        'Programming Language :: Python', # TODO
    ],
    author='John W. Miller',
    author_email='',
    url='https://github.com/johnwmillr/GeniusAPI',
    keywords='genius api music lyrics artists albums songs',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'genius-api = genius.api:main']
    },
)