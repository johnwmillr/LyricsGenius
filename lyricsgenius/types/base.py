import json
from abc import ABC, abstractmethod

from ..utils import sanitize_filename


class BaseEntity(ABC):
    """Base class for types."""

    def __init__(self, id):
        self.id = id

    @abstractmethod
    def to_dict(self):
        """Returns a shallow copy of the object's body."""
        return self._body.copy()

    @abstractmethod
    def to_json(self,
                data,
                filename=None,
                sanitize=True,
                ensure_ascii=True):
        """Converts the object to a json string.

        Args:
            data (:obj:`str`): Data to save (or return if no filename).
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
        with open(filename, 'w') as ff:
            json.dump(data, ff, indent=1, ensure_ascii=ensure_ascii)
        return None

    @abstractmethod
    def to_text(self,
                data,
                filename=None,
                binary_encoding=False,
                sanitize=True):
        """Converts data to a single string.

        Args:
            data (:obj:`str`): Data to save (or return if no filename).
            filename (:obj:`str`, optional): Output filename, a string.
                If not specified, the result is returned as a string.
            binary_encoding (:obj:`bool`, optional): Enables binary encoding
                of text data.
            sanitize (:obj:`bool`, optional): Sanitizes the filename if `True`.

        Returns:
            :obj:`str` \\| ‌:obj:`None`: If :obj:`filename` is `None`,
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
        with open(filename, 'wb' if binary_encoding else 'w') as ff:
            if binary_encoding:
                data = data.encode('utf8')
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
