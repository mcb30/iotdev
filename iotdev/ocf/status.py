"""Response status"""

SHIFT = 5
MASK = (1 << SHIFT) - 1
SUCCESS = 2


class Status():
    """A response status"""

    __slots__ = ['code', 'label']

    registry = {}

    @staticmethod
    def normalise(code):
        """Normalise response code"""
        if isinstance(code, str):
            (major, minor) = code.split('.')
            code = int(major) << SHIFT | int(minor)
        return code

    def __init__(self, code, label=None):
        self.code = self.normalise(code)
        if label is not None:
            self.registry.setdefault(self.code, self)
        elif self.code in self.registry:
            label = self.registry[self.code].label
        self.label = label

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, str(self), self.text)

    def __str__(self):
        return '%d.%02d' % (self.major, self.minor)

    def __int__(self):
        return self.code

    def __bool__(self):
        return self.major == SUCCESS

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if not isinstance(other, Status):
            return NotImplemented
        return self.code == other.code

    @property
    def major(self):
        """Response code major value"""
        return self.code >> SHIFT

    @property
    def minor(self):
        """Response code minor value"""
        return self.code & MASK

    @property
    def success(self):
        """Response code represents success"""
        return bool(self)

    @property
    def text(self):
        """Response code description"""
        return self.label or "%s (%s)" % ("Success" if self else "Error", self)


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
Unimplemented = Status('5.01', "Not Implemented")
BadGateway = Status('5.02', "Bad Gateway")
ServiceUnavailable = Status('5.03', "Service Unavailable")
GatewayTimeout = Status('5.04', "Gateway Timeout")
ProxyingNotSupported = Status('5.05', "Proxying Not Supported")
