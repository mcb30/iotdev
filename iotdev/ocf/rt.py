"""Resource types"""

from itertools import chain
from .property import (BooleanProperty, IntegerProperty, StringProperty,
                       NumericProperty, UUIDProperty, ArrayProperty)

ResourceTypes = {}
"""Registry of named resource types"""


class ResourceTypeMeta(type):
    """Resource type metaclass

    A resource type class may be used as a dictionary in which the
    keys are the property names (which may not match the attribute
    names) and the values are the property objects.
    """

    def __new__(mcl, clsname, bases, namespace, name=None, **kwargs):
        # pylint: disable=bad-mcs-classmethod-argument,protected-access
        namespace['_properties'] = {
            k: v for b in reversed(bases) for k, v in b._properties.items()
        }
        namespace['_rtname'] = name
        cls = super().__new__(mcl, clsname, bases, namespace, **kwargs)
        if name is not None:
            ResourceTypes[name] = cls
        return cls

    #
    # Allow use of ResourceType subclass as a dictionary of Property
    # objects indexed by property name
    #

    def __getitem__(cls, key):
        return cls._properties[key]

    def __setitem__(cls, key, value):
        cls._properties[key] = value

    def __contains__(cls, key):
        return key in cls._properties

    def __iter__(cls):
        return iter(cls._properties)

    def __len__(cls):
        return len(cls._properties)

    #
    # Allow construction from resource type names
    #

    def __lt__(cls, other):
        """Allow resource type classes to be sorted

        Use an ordering that is stable and that results in a
        consistent method resolution order when used as a list of base
        classes.

        This is currently achieved by sorting first by length of the
        MRO tuple (in descending order), then by resource type name
        (in ascending order, with unnamed resource types last), then
        by class name.
        """
        # pylint: disable=protected-access
        return (len(cls.__mro__) > len(other.__mro__) or
                ((cls._rtname is None, cls._rtname, cls.__name__) <
                 (other._rtname is None, other._rtname, other.__name__)))

    def to_rt(cls):
        """Set of resource type names

        This is the (unordered) set of named resource types from which
        the resource type class is constructed.
        """
        if cls._rtname is not None:
            return {cls._rtname}
        rts = (subclass.to_rt() for subclass in cls.__bases__
               if issubclass(subclass, ResourceType))
        return set(chain.from_iterable(rts))

    @staticmethod
    def from_rt(*args):
        """Construct resource type class from resource type name(s)

        Construct a Python class from an unordered list of applicable
        resource type names (e.g. ``['oic.r.switch.binary',
        'oic.r.light.brightness']``).
        """
        bases = sorted(set(ResourceTypes[x] for x in args)) or [ResourceType]
        if len(bases) == 1:
            return bases.pop()
        name = '(%s)' % '+'.join(x.__name__ for x in bases)
        return type(name, tuple(bases), {})

    #
    # Allow construction via arithmetic operators
    #

    def __add__(cls, other):
        # pylint: disable=no-value-for-parameter
        other_rt = (other.to_rt() if isinstance(other, ResourceTypeMeta) else
                    {other} if isinstance(other, str) else
                    set(other))
        return cls.from_rt(*(cls.to_rt() | other_rt))

    def __sub__(cls, other):
        # pylint: disable=no-value-for-parameter
        other_rt = (other.to_rt() if isinstance(other, ResourceTypeMeta) else
                    {other} if isinstance(other, str) else
                    set(other))
        return cls.from_rt(*(cls.to_rt() - other_rt))

    __or__ = __add__

    #
    # Allow issubclass() and isinstance() to use resource type names
    #

    def __subclasscheck__(cls, subclass):
        # pylint: disable=no-value-for-parameter
        return (super().__subclasscheck__(subclass) or
                (isinstance(subclass, ResourceTypeMeta) and
                 subclass.to_rt() >= cls.to_rt()))

    def __instancecheck__(cls, instance):
        # pylint: disable=no-value-for-parameter
        return (super().__instancecheck__(instance) or
                (isinstance(type(instance), ResourceTypeMeta) and
                 type(instance).to_rt() >= cls.to_rt()))


class ResourceType(metaclass=ResourceTypeMeta):
    """Resource type base class

    A resource type object may be used as a dictionary in which the
    keys are the property names (which may not match the attribute
    names) and the values are the current state values.
    """

    _properties = {}
    _rtname = None

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

    def __getitem__(self, key):
        return self._properties[key].__get__(self, type(self))

    def __setitem__(self, key, value):
        self._properties[key].__set__(self, value)

    def __contains__(self, key):
        return key in self._properties

    def __iter__(self):
        return iter(self._properties)

    def __len__(self):
        return len(self._properties)


class Device(ResourceType, name='oic.wk.d'):
    """A device"""

    di = UUIDProperty(writable=False)


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


class Temperature(ResourceType, name='oic.r.temperature'):
    """A temperature sensor"""

    temperature = NumericProperty(writable=False)
