"""Resource types"""

from collections import UserDict
from .property import (BooleanProperty, IntegerProperty, StringProperty,
                       ArrayProperty)


class ResourceTypeRegistry(UserDict):
    """Registry of resource types"""

    def register(self, cls):
        """Register resource type class"""
        self.data[cls.__name__] = cls

    def type(self, *args):
        """Construct resource class from resource type name(s)

        Construct a Python class from an unordered list of applicable
        resource type names (e.g. ``['oic.r.switch.binary',
        'oic.r.light.brightness']``).
        """

        # Construct unordered set of base types
        bases = set(self[x] for x in args) or {ResourceType}

        # Use existing type if only a single base type is specified
        if len(bases) == 1:
            return bases.pop()

        # Canonicalise order by MRO length (to ensure a consistent
        # MRO, if possible), then by name
        bases = sorted(bases, key=lambda x: (-len(x.__mro__), x.__name__))

        # Construct new type
        name = '[%s]' % ','.join(x.__name__ for x in bases)
        return type(name, tuple(bases), {})


ResourceTypes = ResourceTypeRegistry()


class ResourceType():
    """Resource type base class"""

    n = StringProperty(meta=True)
    id = StringProperty(meta=True, writable=False)
    rt = ArrayProperty[StringProperty](meta=True, required=True,
                                       writable=False)
    if_ = ArrayProperty[StringProperty](name="if", meta=True, required=True,
                                        writable=False)

    def __init__(self, resource):
        self.resource = resource

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.resource)

    def __init_subclass__(cls, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if name is not None:
            cls.__name__ = cls.__qualname__ = name
        ResourceTypes.register(cls)


class BinarySwitch(ResourceType, name='oic.r.switch.binary'):
    """A binary switch (on/off)"""

    value = BooleanProperty()


class Brightness(ResourceType, name='oic.r.light.brightness'):
    """The brightness of a light or lamp"""

    brightness = IntegerProperty()


class Refrigeration(ResourceType, name='oic.r.refrigeration'):
    """A refrigeration function"""

    filter = IntegerProperty(writable=False)
    rapidFreeze = BooleanProperty()
    rapidCool = BooleanProperty()
    defrost = BooleanProperty()
