"""Resources"""

from collections import UserDict
from .rt import ResourceTypes


class Resource(UserDict):
    """A resource

    A resource is a representation of a physical entity (such as a
    temperature sensor).
    """

    def __init__(self, data):
        super().__init__(data)
        self._type = None

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key == 'rt':
            self._type = None

    @property
    def type(self):
        """Construct resource class from `rt` state value"""
        if self._type is None:
            rt = self.data.get('rt', ())
            self._type = ResourceTypes.type(*rt)
        return self._type

    @property
    def r(self):
        """Typed resource

        This object provides named-attribute access to state values.
        Its class is dynamically constructed based on the `rt` state
        value.
        """
        # pylint: disable=not-callable
        return self.type(self)
