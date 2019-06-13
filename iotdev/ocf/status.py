"""Response status"""

import re

SHIFT = 5
MASK = (1 << SHIFT) - 1
SUCCESS = 2

Statuses = {}
"""Response status class registry"""


class StatusCodeBase(int):
    """Response status code"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    @property
    def major(self):
        """Response code major value"""
        return self >> SHIFT

    @property
    def minor(self):
        """Response code minor value"""
        return self & MASK

    @property
    def success(self):
        """Response code represents success"""
        return self.major == SUCCESS


class StatusCodeCategory(StatusCodeBase):
    """Response status code category (e.g. '2.xx')"""

    category = None
    minor = None

    def __new__(cls, value, **kwargs):
        if isinstance(value, str):
            (major, _) = value.split('.')
            value = int(major) << SHIFT
        return super().__new__(cls, value, **kwargs)

    def __str__(self):
        return '%d.xx' % self.major


class StatusCode(StatusCodeBase):
    """Response status code (e.g. '2.01')"""

    def __new__(cls, value, **kwargs):
        if isinstance(value, str):
            (major, minor) = value.split('.')
            value = int(major) << SHIFT | int(minor)
        return super().__new__(cls, value, **kwargs)

    def __str__(self):
        return '%d.%02d' % (self.major, self.minor)

    @property
    def category(self):
        """Response code category"""
        return StatusCodeCategory(self & ~MASK)


class StatusMeta(type):
    """Response status metaclass"""

    code = None
    label = None

    def __new__(mcl, name, bases, namespace, code=None, label=None, **kwargs):
        # pylint: disable=bad-mcs-classmethod-argument
        # pylint: disable=too-many-arguments, unused-argument
        return super().__new__(mcl, name, bases, namespace, **kwargs)

    def __init__(cls, name, bases, namespace, code=None, label=None, **kwargs):
        # pylint: disable=too-many-arguments
        super().__init__(name, bases, namespace, **kwargs)
        if code is not None:
            cls.code = code
        if label is not None:
            cls.label = label

    def __repr__(cls):
        if cls.code is None:
            return super().__repr__()
        builder = Status if cls.code.category else StatusCategory
        return '%s(%r, %r)' % (builder.__name__, str(cls), cls.text)

    def __str__(cls):
        return str(cls.code)

    def __int__(cls):
        return cls.code

    def __bool__(cls):
        return cls.code.success

    def __hash__(cls):
        return hash(cls.code)

    @property
    def major(cls):
        """Response code major value"""
        return cls.code.major

    @property
    def minor(cls):
        """Response code minor value"""
        return cls.code.minor

    @property
    def success(cls):
        """Response code represents success"""
        return cls.code.success

    @property
    def category(cls):
        """Response code category"""
        return cls.code.category

    @property
    def text(cls):
        """Response code description"""
        return (
            cls.label or
            "%s (%s)" % ("Success" if cls.code.success else "Error", cls)
        )


class StatusBase(metaclass=StatusMeta):
    """Response status base class"""

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    def __str__(self):
        return str(type(self))

    def __int__(self):
        return int(type(self))

    def __bool__(self):
        return bool(type(self))

    def __hash__(self):
        return hash(type(self))

    @property
    def major(self):
        """Response code major value"""
        return type(self).major

    @property
    def minor(self):
        """Response code minor value"""
        return type(self).minor

    @property
    def success(self):
        """Response code represents success"""
        return type(self).success

    @property
    def category(self):
        """Response code category"""
        return type(self).category

    @property
    def text(self):
        """Response code description"""
        return type(self).text


class StatusException(Exception, StatusBase):
    """Failure response status base class"""

    def __str__(self):
        return super().__str__() if self.args else self.text


def Status(code, label=None):
    """Construct a response status class"""
    if not isinstance(code, StatusCodeBase):
        code = StatusCode(code)
    cls = Statuses.get((code.major, code.minor))
    if cls is None:
        name = re.sub(r'\W+', '', label or ("Status%s" % code))
        bases = [StatusBase if code.success else StatusException]
        if code.category is not None:
            bases.insert(0, Status(code.category))
        cls = type(name, tuple(bases), {}, code=code, label=label)
        # Ensure that only one class ever exists for a given code,
        # since try..except relies on identity comparisons
        cls = Statuses.setdefault((code.major, code.minor), cls)
    return cls


def StatusCategory(code, label=None):
    """Construct a response status category class"""
    return Status(StatusCodeCategory(code), label=label)


ClientError = StatusCategory('4.xx', "Client Error")
ServerError = StatusCategory('5.xx', "Server Error")

Created = Status('2.01', "Created")
Deleted = Status('2.02', "Deleted")
Valid = Status('2.03', "Valid")
Changed = Status('2.04', "Changed")
Content = Status('2.05', "Content")
Continue = Status('2.31', "Continue")
BadRequest = Status('4.00', "Bad Request")
Unauthorized = Status('4.01', "Unauthorized")
BadOption = Status('4.02', "Bad Option")
Forbidden = Status('4.03', "Forbidden")
NotFound = Status('4.04', "Not Found")
MethodNotAllowed = Status('4.05', "Method Not Allowed")
NotAcceptable = Status('4.06', "Not Acceptable")
RequestEntityIncomplete = Status('4.08', "Request Entity Incomplete")
Conflict = Status('4.09', "Conflict")
PreconditionFailed = Status('4.12', "Precondition Failed")
RequestEntityTooLarge = Status('4.13', "Request Entity Too Large")
UnsupportedContentFormat = Status('4.15', "Unsupported Content-Format")
UnprocessableEntity = Status('4.22', "Unprocessable Entity")
TooManyRequests = Status('4.29', "Too Many Requests")
InternalServerError = Status('5.00', "Internal Server Error")
MethodNotImplemented = Status('5.01', "Method Not Implemented")
BadGateway = Status('5.02', "Bad Gateway")
ServiceUnavailable = Status('5.03', "Service Unavailable")
GatewayTimeout = Status('5.04', "Gateway Timeout")
ProxyingNotSupported = Status('5.05', "Proxying Not Supported")
