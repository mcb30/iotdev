"""Resource state"""

from collections import defaultdict, UserDict
from .json import JSONEncoder, JSONDecoder


class ResourceState(UserDict):
    """Resource state representation

    This is a raw resource state dictionary, as produced by
    deserialising a JSON or CBOR representation of the resource state.
    """

    json_encoder = JSONEncoder()
    json_decoder = JSONDecoder()

    def __init__(self, data=None, json=None):
        super().__init__(data)
        if json is not None:
            if data is not None:
                raise TypeError("Specify at most one of 'data' or 'json'")
            self.json = json

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.data)

    @property
    def json(self):
        """JSON serialisation of resource state"""
        return self.json_encoder.encode(self.data)

    @json.setter
    def json(self, data):
        # pylint: disable=attribute-defined-outside-init
        self.data = self.json_decoder.decode(data)


class TrackedResourceState(ResourceState):
    """Resource state representation with change tracking support"""

    def __init__(self, data=None, json=None):
        self.tracked = defaultdict(list)
        super().__init__(data=data, json=json)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key in self.tracked:
            for callback in self.tracked[key]:
                callback()

    def __delitem__(self, key):
        super().__delitem__(key)
        if key in self.tracked:
            for callback in self.tracked[key]:
                callback()

    def track(self, key, callback):
        """Track changes"""
        self.tracked[key].append(callback)
