from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agenius",
    version="1.0",
    description="A LyricsGenius fork with async ready features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dopebnan/Genius.py",
    project_urls={
        "Bug Tracker": "https://github.com/dopebnan/Genius.py/issues"
    },
    author="dopebnan",
    author_email="82271322+dopebnan@users.noreply.github.com",
    license="LGPLv3",
    package_dir={"": "agenius-py"},
    python_requires=">=3.9",
    install_requires=[
        "beautifulsoup4>=4.6.0",
        "aiohttp>=3.6.0,<4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent"
    ]
)
