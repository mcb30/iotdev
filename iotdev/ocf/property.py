"""Resource properties"""

from uuid import UUID


class Property():
    """A resource property

    A property describes a single aspect of a resource.  For example:
    the property `n` describes the resource name, the property `rt`
    describes the resource type(s), and the property `temperature`
    might describe the current value of a resource's temperature
    sensor.
    """

    def __init__(self, name=None, meta=False, required=False, readable=True,
                 writable=True, default=None):
        # pylint: disable=too-many-arguments

        self.name = name
        """Property name

        This may be omitted, in which case the descriptor name will be
        used.
        """

        self.meta = meta
        """Property is metadata

        Metadata properties (such as `n` and `rt`) are used to
        describe the resource itself, in contrast to operational
        properties (such as `temperature`) which describe the current
        state of the resource.
        """

        self.required = required
        """Property is mandatory"""

        self.readable = readable
        """Property value may be read"""

        self.writable = writable
        """Property value may be written"""

        self.default = default
        """Default value"""

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


class UUIDProperty(Property):
    """A UUID-valued property"""

    @staticmethod
    def canonicalise(state):
        return state if isinstance(state, UUID) else UUID(state)


class ArrayPropertyMeta(type):
    """Array-valued property metaclass"""

    def __getitem__(cls, key):
        """Construct array-valued property for specified entry type"""
        name = '%s[%s]' % (cls.__name__, key.__name__)
        return type(name, (cls,), {'subtype': key})


class ArrayProperty(Property, metaclass=ArrayPropertyMeta):
    """An array-valued property"""

    subtype = Property

    def canonicalise(self, state):
        return tuple(self.subtype.canonicalise(x) for x in state)
