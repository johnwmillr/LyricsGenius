from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agenius",
    version="4.0.1",
    description="A LyricsGenius fork with async ready features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dopebnan/AGenius.py",
    project_urls={
        "Bug Tracker": "https://github.com/dopebnan/AGenius.py/issues"
    },
    author="dopebnan",
    author_email="82271322+dopebnan@users.noreply.github.com",
    license="LGPLv3+",
    packages=["agenius", "agenius.api_calls", "agenius.class_types"],
    python_requires=">=3.7",
    install_requires=[
        "beautifulsoup4>=4.6.0",
        "aiohttp>=3.6.0,<4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"
    ]
)
