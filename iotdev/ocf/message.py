"""Messages"""

from abc import ABC, abstractmethod
from multidict import MultiDict
from .state import ResourceState
from .status import Created, Deleted, Changed, Content

RequestTypes = {}


class Message(ABC):
    """A message"""

    def __init__(self, data=None, *, json=None, state=None, token=None):
        if data is not None or json is not None:
            if state is not None:
                raise TypeError("Specify at most one of 'data', 'json', "
                                "or 'state'")
            state = ResourceState(data=data, json=json)
        self.state = state
        self.token = token

    @property
    def json(self):
        """State serialised as JSON"""
        return self.state.json if self.state is not None else None

    @json.setter
    def json(self, value):
        self.state = ResourceState(json=value) if value else None


class Request(Message):
    """A request message"""

    def __init__(self, uri, data=None, *, json=None, state=None, token=None,
                 params=()):
        super().__init__(data=data, json=json, state=state, token=token)
        self.uri = uri
        self.params = MultiDict(params)

    def __repr__(self):
        return '%s(%r%s)' % (self.__class__.__name__, self.uri, ''.join((
            ', state=%r' % self.state if self.state is not None else '',
            ', token=%r' % self.token if self.token is not None else '',
            ', params=%r' % list(self.params.items()) if self.params else '',
        )))

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        RequestTypes[cls.method] = cls

    @property
    @abstractmethod
    def method(self):
        """Request method"""
        pass

    @property
    @abstractmethod
    def success(self):
        """Success status"""
        pass


class Create(Request):
    """A CREATE message"""

    method = 'CREATE'
    success = Created


class Retrieve(Request):
    """A RETRIEVE message"""

    method = 'RETRIEVE'
    success = Content


class Update(Request):
    """An UPDATE message"""

    method = 'UPDATE'
    success = Changed


class Delete(Request):
    """A DELETE message"""

    method = 'DELETE'
    success = Deleted


class Notify(Request):
    """A NOTIFY message"""

    method = 'NOTIFY'
    success = Content


class Response(Message):
    """A response message"""

    def __init__(self, status, data=None, *, json=None, state=None,
                 token=None):
        super().__init__(data=data, json=json, state=state, token=token)
        self.status = status

    def __repr__(self):
        return '%s(%r%s)' % (self.__class__.__name__, self.status, ''.join((
            ', state=%r' % self.state if self.state is not None else '',
            ', token=%r' % self.token if self.token is not None else '',
        )))
