from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Base class for types."""

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        name = self.__class__.__name__
        attrs = [
            x for x in list(self.__dict__.keys()) if not x.startswith('_')
        ]
        attrs = ", ".join(attrs[:2])
        return f"{name}({attrs}, ...)"
