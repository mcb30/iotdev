"""Resources"""

from collections import UserDict
from collections.abc import Mapping
from types import MappingProxyType
from .interface import Interfaces, BaselineInterface
from .rt import ResourceType, ResourceTypeMeta


class ResourceState(UserDict):
    """Raw resource state

    This is the raw state dictionary as produced by deserialising a
    JSON or CBOR representation of the resource state.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_rt = None

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key == 'rt':
            self.cached_rt = None


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
        return key in self.resource.state.get('if', ())

    def __iter__(self):
        return iter(self.resource.state.get('if', ()))

    def __len__(self):
        return len(self.resource.state.get('if', ()))


class Resource():
    """A resource

    A resource is a representation of a physical entity (such as a
    temperature sensor).
    """

    default_intf = BaselineInterface

    def __init__(self, state=None):
        self.state = ResourceState(state)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.state)

    @property
    def rt(self):
        """Resource type

        This is the Python class dynamically constructed based on the
        `rt` state value.
        """
        state = self.state
        if state.cached_rt is None:
            rt = state.get('rt', ())
            state.cached_rt = ResourceType.from_rt(*rt)
        return state.cached_rt

    @rt.setter
    def rt(self, value):
        """Set resource type"""
        self.state['rt'] = (
            value.to_rt() if isinstance(value, ResourceTypeMeta)
            else value
        )

    @rt.deleter
    def rt(self):
        """Clear resource type"""
        self.state['rt'] = ()

    @property
    def prop(self):
        """Resource properties

        This object provides both dictionary and named-attribute
        access to resource property values.  The class of this object
        is dynamically constructed based on the `rt` state value(s).
        """
        # pylint: disable=not-callable
        return self.rt(self)

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

    def retrieve(self, params=MappingProxyType({})):
        """Retrieve resource representation"""
        intf = self.intf[params.get('if', self.default_intf.__name__)]
        return intf.retrieve(params)

    def update(self, data, params=MappingProxyType({})):
        """Update resource representation"""
        intf = self.intf[params.get('if', self.default_intf.__name__)]
        intf.update(data, params)

    def load(self, names, params):
        """Load resource properties"""
        pass

    def save(self, names, params):
        """Save resource properties"""
        pass
