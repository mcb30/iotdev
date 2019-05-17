"""Interfaces

An interface defines a subset of accessible properties on a resource,
and a corresponding list of permitted requests and responses.
"""

from .exceptions import OcfBadRequest

Interfaces = {}
"""Registry of named interfaces"""


class Interface():
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

    def retrieve(self):
        """Retrieve resource representation"""
        prop = self.resource.prop
        # Retrieve visible and readable properties
        data = {k: prop[k] for k in prop if
                type(prop)[k].readable and self.visible(type(prop)[k])}
        return data

    def update(self, data):
        """Update resource representation"""
        prop = self.resource.prop
        # Ignore any properties not visible via this interface
        data = {k: v for k, v in data.items() if self.visible(type(prop)[k])}
        # Fail on an attempt to update any read-only properties
        readonly = [k for k in data if not type(prop)[k].writable]
        if readonly:
            raise OcfBadRequest('Not writable: %s' % ', '.join(readonly))
        # Update visible and writable properties
        for k, v in data.items():
            prop[k] = v


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
