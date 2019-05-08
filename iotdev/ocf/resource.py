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
        self._prop_type = None

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key == 'rt':
            self._prop_type = None

    @property
    def prop(self):
        """Resource properties

        This object provides named-attribute access to resource
        property values.  The class of this object is dynamically
        constructed based on the `rt` state value(s).
        """
        if self._prop_type is None:
            rt = self.data.get('rt', ())
            self._prop_type = ResourceTypes.type(*rt)
        return self._prop_type(self)
