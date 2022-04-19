from abc import ABC


class BaseEntity(ABC):
    """Base class for types."""

    def __init__(self, _id):
        self.id = _id

    def __repr__(self):
        name = self.__class__.__name__
        attrs = [
            x for x in list(self.__dict__.keys()) if not x.startswith('_')
        ]
        attrs = ", ".join(attrs[:2])
        return f"{name}({attrs}, ...)"
