"""Interfaces

An interface defines a subset of accessible properties on a resource,
and a corresponding list of permitted requests and responses.
"""

from types import MappingProxyType
from .exceptions import OcfBadRequest

Interfaces = {}
"""Registry of named interfaces"""


class InterfaceMeta(type):
    """Interface metaclass"""

    def __str__(cls):
        return cls.__name__


class Interface(metaclass=InterfaceMeta):
    """Interface base class"""

    def __init__(self, resource):

        self.resource = resource
        """Resource accessed through this interface"""

    def __init_subclass__(cls, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if name is not None:
            cls.__name__ = cls.__qualname__ = name
        Interfaces[cls.__name__] = cls

    @staticmethod
    def visible(prop):
        """Check visibility of property via this interface"""
        raise NotImplementedError

    def retrieve(self, params=MappingProxyType({})):
        """Retrieve resource representation"""
        prop = self.resource.prop
        meta = type(prop)
        # Determine visible and readable properties
        names = [x for x in meta if meta[x].readable and self.visible(meta[x])]
        # Load required property values
        self.resource.load(names, params)
        # Retrieve visible, readable, and existent (or required) properties
        return {x: prop[x] for x in names if x in prop or meta[x].required}

    def update(self, data, params=MappingProxyType({})):
        """Update resource representation"""
        prop = self.resource.prop
        meta = type(prop)
        # Determine visible properties
        names = [x for x in data if self.visible(meta[x])]
        # Fail on an attempt to update any read-only properties
        readonly = [x for x in names if not meta[x].writable]
        if readonly:
            raise OcfBadRequest('Not writable: %s' % ', '.join(readonly))
        # Update visible and writable properties
        for name in names:
            prop[name] = data[name]
        # Save property values
        self.resource.save(names, params)


class BaselineInterface(Interface, name='oic.if.baseline'):
    """Baseline interface

    Provides access to all properties of a resource (including common
    properties).
    """

    @staticmethod
    def visible(prop):
        return True


class ActuatorInterface(Interface, name='oic.if.a'):
    """Actuator interface

    Provides access to operational writable properties of a resource
    (such as the set point temperature for a thermostat).
    """

    @staticmethod
    def visible(prop):
        return prop.writable and not prop.meta


class SensorInterface(Interface, name='oic.if.s'):
    """Sensor interface

    Provides access to operational read-only properties of a resource
    (such as the current temperature of a thermostat).
    """

    @staticmethod
    def visible(prop):
        return not prop.writable and not prop.meta


class ReadOnlyInterface(Interface, name='oic.if.r'):
    """Read-only interface

    Provides access to all read-only properties of a resource.
    """

    @staticmethod
    def visible(prop):
        return not prop.writable


class ReadWriteInterface(Interface, name='oic.if.rw'):
    """Read-write interface

    Provides access to all writable properties of a resource.
    """

    @staticmethod
    def visible(prop):
        return prop.writable
