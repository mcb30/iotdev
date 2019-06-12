"""Endpoints"""

from functools import total_ordering
from urllib.parse import urlparse
from .transport import Transports


@total_ordering
class Endpoint():
    """An endpoint

    An endpoint is a connection point through which a resource may be
    accessed.
    """

    def __init__(self, uri, priority=1):
        self.uri = uri
        self.scheme = urlparse(uri).scheme
        if not self.scheme:
            raise ValueError("Endpoint uri URI is not absolute")
        self.priority = priority

    def __repr__(self):
        return '%s(%r, priority=%r)' % (self.__class__.__name__, self.uri,
                                        self.priority)

    def __eq__(self, other):
        """Allow equivalent endpoints to be compared as equal"""
        if not isinstance(other, Endpoint):
            return NotImplemented
        return (self.priority, self.uri) == (other.priority, other.uri)

    def __lt__(self, other):
        """Allow endpoints to be sorted

        Sort by priority (a lower numeric priority value is a higher
        priority endpoint), then by name (to produce a stable
        ordering).
        """
        if not isinstance(other, Endpoint):
            return NotImplemented
        return (self.priority, self.uri) < (other.priority, other.uri)

    @property
    def transport(self):
        """Default transport"""
        return Transports[self.scheme]

    def dispatch(self, msg, transport=None):
        """Dispatch message"""
        if transport is None:
            transport = self.transport
        return transport.dispatch(self, msg)
