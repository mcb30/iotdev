"""Resource properties"""

from uuid import UUID
from orderedset import OrderedSet

Unspecified = object()


class Property():
    """A resource property

    A property describes a single aspect of a resource.  For example:
    the property `n` describes the resource name, the property `rt`
    describes the resource type(s), and the property `temperature`
    might describe the current value of a resource's temperature
    sensor.
    """

    meta = False
    """Property is metadata

    Metadata properties (such as `n` and `rt`) are used to describe
    the resource itself, in contrast to operational properties (such
    as `temperature`) which describe the current state of the
    resource.
    """

    required = False
    """Property is mandatory"""

    readable = True
    """Property value may be read"""

    writable = True
    """Property value may be written"""

    default = None
    """Default value"""

    def __init__(self, name=None, meta=Unspecified, required=Unspecified,
                 readable=Unspecified, writable=Unspecified,
                 default=Unspecified):
        # pylint: disable=too-many-arguments

        self.name = name
        """Property name

        This may be omitted, in which case the descriptor name will be
        used.
        """

        if meta is not Unspecified:
            self.meta = meta
        if required is not Unspecified:
            self.required = required
        if readable is not Unspecified:
            self.readable = readable
        if writable is not Unspecified:
            self.writable = writable
        if default is not Unspecified:
            self.default = default

    def __get__(self, instance, owner):
        """Get value"""
        if instance is None:
            return self
        try:
            state = instance.resource.state[self.name]
        except KeyError:
            return self.default
        return self.canonicalise(state)

    def __set__(self, instance, value):
        """Set value"""
        state = self.canonicalise(value)
        instance.resource.state[self.name] = state

    def __delete__(self, instance):
        """Delete value"""
        del instance.resource.state[self.name]

    def __set_name__(self, owner, name):
        """Set descriptor name"""
        if self.name is None:
            self.name = name
        owner[self.name] = self

    @staticmethod
    def canonicalise(state):
        """Convert to canonical type"""
        return state


class BooleanProperty(Property):
    """A boolean-valued property"""

    canonicalise = bool


class IntegerProperty(Property):
    """An integer-valued property"""

    canonicalise = int


class StringProperty(Property):
    """A string-valued property"""

    canonicalise = str


class NumericProperty(Property):
    """An integer- or float-valued property"""

    @staticmethod
    def canonicalise(state):
        return state + 0


class UUIDProperty(Property):
    """A UUID-valued property"""

    @staticmethod
    def canonicalise(state):
        return state if isinstance(state, UUID) else UUID(state)


class ContainerPropertyMeta(type):
    """Container property metaclass"""

    def __getitem__(cls, key):
        """Construct container property for specified entry type"""
        name = '%s[%s]' % (cls.__name__, key.__name__)
        return type(name, (cls,), {'element': key})


class ArrayProperty(Property, metaclass=ContainerPropertyMeta):
    """An array-valued property"""

    element = Property

    default = tuple()

    def canonicalise(self, state):
        return tuple(self.element.canonicalise(x) for x in state)


class OrderedSetProperty(Property, metaclass=ContainerPropertyMeta):
    """An ordered set-valued property"""

    element = Property

    @property
    def default(self):
        """Default value"""
        return OrderedSet()

    def canonicalise(self, state):
        return OrderedSet(self.element.canonicalise(x) for x in state)
