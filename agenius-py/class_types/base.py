"""
Copyright (C) 2022 dopebnan
This file is part of AGenius.py.
You should have received a copy of the GNU Lesser General Public License along with AGenius.py.
If not, see <https://www.gnu.org/licenses/>.
"""

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
