"""Resources"""

from collections import UserDict
from collections.abc import Mapping
from .interface import Interfaces
from .rt import ResourceTypes


class ResourceInterfaces(Mapping):
    """All interfaces onto a resource"""

    __slots__ = ['resource']

    def __init__(self, resource):

        self.resource = resource
        """The resource accessed through these interfaces"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.resource)

    def __getitem__(self, key):
        return Interfaces[key](self.resource)

    def __contains__(self, key):
        return key in self.resource.get('if', ())

    def __iter__(self):
        return iter(self.resource.get('if', ()))

    def __len__(self):
        return len(self.resource.get('if', ()))


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

        This object provides both dictionary and named-attribute
        access to resource property values.  The class of this object
        is dynamically constructed based on the `rt` state value(s).
        """
        if self._prop_type is None:
            rt = self.data.get('rt', ())
            self._prop_type = ResourceTypes.type(*rt)
        return self._prop_type(self)

    @property
    def intf(self):
        """Resource interfaces

        This is a dictionary of all supported interfaces onto the
        resource.  Dictionary keys are interface names such as
        `oic.if.baseline`.  Dictionary values are interface objects
        (of the corresponding `Interface` subclass) attached to the
        resource.
        """
        return ResourceInterfaces(self)
