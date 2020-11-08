import json
import os
from abc import ABC, abstractmethod

from ..utils import safe_unicode, sanitize_filename


class BaseEntity(ABC):
    """Base class for types."""

    def __init__(self, id):
        self.id = id

    @abstractmethod
    def save_lyrics(self,
                    filename,
                    extension='json',
                    overwrite=False,
                    ensure_ascii=True,
                    sanitize=True,
                    verbose=True):
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
            invalid characters, and thefore cause the saving to fail.

        """
        extension = extension.lstrip(".").lower()
        msg = "extension must be JSON or TXT"
        assert (extension == 'json') or (extension == 'txt'), msg

        # Determine the filename
        for ext in [".txt", ".TXT", ".json", ".JSON"]:
            if ext in filename:
                filename = filename.replace(ext, "")
                break
        filename += "." + extension
        filename = sanitize_filename(filename) if sanitize else filename

        # Check if file already exists
        write_file = False
        if overwrite or not os.path.isfile(filename):
            write_file = True
        elif verbose:
            msg = "{} already exists. Overwrite?\n(y/n): ".format(filename)
            if input(msg).lower() == 'y':
                write_file = True

        # Exit if we won't be saving a file
        if not write_file:
            if verbose:
                print('Skipping file save.\n')
            return

        # Save the lyrics to a file
        if extension == 'json':
            self.to_json(filename, ensure_ascii=ensure_ascii, sanitize=sanitize)
        else:
            self.to_text(filename, sanitize=sanitize)

        if verbose:
            print('Wrote {}.'.format(safe_unicode(filename)))

        return None

    @abstractmethod
    def to_dict(self):
        """Converts the object to a dictionary."""
        return self._body.copy()

    @abstractmethod
    def to_json(self,
                data,
                filename=None,
                sanitize=True,
                ensure_ascii=True):
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
        with open(filename, 'w', encoding='utf-8') as ff:
            json.dump(data, ff, indent=1, ensure_ascii=ensure_ascii)
        return None

    @abstractmethod
    def to_text(self,
                data,
                filename=None,
                sanitize=True):
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
            return data

        # Save song lyrics to a text file
        filename = sanitize_filename(filename) if sanitize else filename
        with open(filename, 'w', encoding='utf-8') as ff:
            ff.write(data)
        return None

    def __repr__(self):
        name = self.__class__.__name__
        attrs = [x
                 for x in list(self.__dict__.keys())
                 if not x.startswith('_')]
        attrs = ', '.join(attrs[:2])
        return "{}({}, ...)".format(name, attrs)


class Stats(object):
    """Stats of an item.

    Note:
        The values passed to this class are inconsistent,
        and therefore need to be set dynamically.
        Use the built-in ``dir()`` function to
        see the available attributes.
        You could also access the stats by the dictionary
        annotation. For example:

        .. code:: python

            values = song.to_dict()
            print(values['stats'])

    """

    def __init__(self, json_dict):

        for key, value in json_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        name = self.__class__.__name__
        attrs = ', '.join(list(self.__dict__.keys()))
        return "{}({!r})".format(name, attrs)

# class EntityWithLyrics(ABC, BaseEntity):
#    """Entity that has lyrics."""
#
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#
#    @abstractmethod
#    def save_lyrics(self):
#        pass
