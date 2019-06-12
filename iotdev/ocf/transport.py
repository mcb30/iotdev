"""Transports"""

from abc import ABC, abstractmethod
from collections import UserDict


class TransportRegistry(UserDict):
    """Registry of default transports"""

    def register(self, transport):
        """Register default transport"""
        for scheme in transport.schemes:
            self[scheme] = transport

Transports = TransportRegistry()


class Transport(ABC):
    """A transport

    A transport is a means of communicating via a particular protocol
    family.
    """

    schemes = ()
    """Supported URI schemes"""

    @abstractmethod
    def dispatch(self, ep, msg):
        """Dispatch message via an endpoint"""
        pass
