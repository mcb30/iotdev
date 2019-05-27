"""Resources"""

from collections.abc import Mapping
from types import MappingProxyType
from .interface import Interfaces, BaselineInterface
from .rt import ResourceType, ResourceTypeMeta
from .state import TrackedResourceState


class ResourceInterfaces(Mapping):
    """All interfaces onto a resource"""

    __slots__ = ['resource']

    def __init__(self, resource):

        self.resource = resource
        """The resource accessed through these interfaces"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.resource)

    def __getitem__(self, key):
        return Interfaces[str(key)](self.resource)

    def __contains__(self, key):
        return str(key) in self.resource.state.get('if', ())

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
        self.cached_rt = None
        self.state = TrackedResourceState(state)
        self.state.track('rt', self.clear_cached_rt)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.state)

    def clear_cached_rt(self):
        """Clear cached resource type"""
        self.cached_rt = None

    @property
    def rt(self):
        """Resource type

        This is the Python class dynamically constructed based on the
        `rt` state value.
        """
        if self.cached_rt is None:
            rt = self.state.get('rt', ())
            self.cached_rt = ResourceType.from_rt(*rt)
        return self.cached_rt

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
        intf = self.intf[params.get('if', self.default_intf)]
        return intf.retrieve(params)

    def update(self, data, params=MappingProxyType({})):
        """Update resource representation"""
        intf = self.intf[params.get('if', self.default_intf)]
        intf.update(data, params)

    def load(self, names, params):
        """Load resource properties"""
        pass

    def save(self, names, params):
        """Save resource properties"""
        pass
