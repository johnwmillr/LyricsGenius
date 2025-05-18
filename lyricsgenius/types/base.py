import json
import os
from abc import ABC, abstractmethod
from typing import Any

from ..utils import safe_unicode, sanitize_filename


class BaseEntity(ABC):
    """Base class for Genius data types (e.g. Song, Artist, album)."""

    @abstractmethod
    def save_lyrics(
        self,
        filename: str,
        extension: str = "json",
        overwrite: bool = False,
        ensure_ascii: bool = True,
        sanitize: bool = True,
        verbose: bool = True,
    ) -> None:
        """Save Song(s) lyrics and metadata to a JSON or TXT file.

        If the extension is 'json' (the default), the lyrics will be saved
        alongside the song's information. Take a look at the example below.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            extension (:obj:`str`, optional): Format of the file (`json` or `txt`).
            overwrite (:obj:`bool`, optional): Overwrites preexisting file if `True`.
                Otherwise prompts user for input.
            ensure_ascii (:obj:`bool`, optional): If ensure_ascii is true
                (the default), the output is guaranteed to have all incoming
                non-ASCII characters escaped.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.
            verbose (:obj:`bool`, optional): prints operation result.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and therefore cause the saving to fail.

        """
        extension = extension.lstrip(".").lower()
        msg = "extension must be JSON or TXT"
        assert (extension == "json") or (extension == "txt"), msg

        # Standardize the extension
        filename, _ = os.path.splitext(filename)
        filename += "." + extension
        filename = sanitize_filename(filename) if sanitize else filename

        # Check if file already exists
        write_file = False
        if overwrite or not os.path.isfile(filename):
            write_file = True
        elif verbose:
            msg = "{} already exists. Overwrite?\n(y/n): ".format(filename)
            if input(msg).lower() == "y":
                write_file = True

        # Exit if we won't be saving a file
        if not write_file:
            if verbose:
                print("Skipping file save.\n")
            return

        # Save the lyrics to a file
        if extension == "json":
            self.to_json(filename, ensure_ascii=ensure_ascii, sanitize=sanitize)
        else:
            self.to_text(filename, sanitize=sanitize)

        if verbose:
            print("Wrote {}.".format(safe_unicode(filename)))

        return None

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Converts the object to a dictionary."""
        if hasattr(self, "_body"):
            return self._body.copy()
        return {}

    @abstractmethod
    def to_json(
        self,
        filename: str | None = None,
        sanitize: bool = True,
        ensure_ascii: bool = True,
    ) -> str | None:
        """Converts the object to a json string.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.
            ensure_ascii (:obj:`bool`, optional): If ensure_ascii is true
              (the default), the output is guaranteed to have all incoming
              non-ASCII characters escaped.

        Returns:
            :obj:`str` \\|‌ :obj:`None`: If :obj:`filename` is `None`,
            returns the lyrics as a plain string, otherwise `None`.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and therefore cause the saving to fail.

        """
        data = self.to_dict()

        # Return the json string if no output path was specified
        if not filename:
            return json.dumps(data, indent=1, ensure_ascii=ensure_ascii)

        # Save Song object to a json file
        filename = sanitize_filename(filename) if sanitize else filename
        with open(filename, "w", encoding="utf-8") as ff:
            json.dump(data, ff, indent=4, ensure_ascii=ensure_ascii)
        return None

    @property
    def _text_data(self) -> str:
        """
        Returns the text data for the entity.

        Different subclasses will implement this method differently.
        For example, the Song class will return lyrics for just one
        song, while the Album class will return the lyrics for all songs
        in the album concatenated together.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_text(self, filename: str | None = None, sanitize: bool = True) -> str | None:
        """Converts song(s) lyrics to a single string.

        Args:
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.

        Returns:
            :obj:`str` \\|‌ :obj:`None`: If :obj:`filename` is `None`,
            returns the lyrics as a plain string. Otherwise `None`.

        Warning:
            If you set :obj:`sanitize` to `False`, the file name may contain
            invalid characters, and therefore cause the saving to fail.

        """
        # Return the lyrics as a string if no `filename` was specified
        if not filename:
            return self._text_data

        # Save song lyrics to a text file
        filename = sanitize_filename(filename) if sanitize else filename
        with open(filename, "w", encoding="utf-8") as ff:
            ff.write(self._text_data)
        return None

    def __repr__(self) -> str:
        name = self.__class__.__name__
        attrs = ", ".join(
            [x for x in list(self.__dict__.keys()) if not x.startswith("_")][:2]
        )
        return "{}({}, ...)".format(name, attrs)
