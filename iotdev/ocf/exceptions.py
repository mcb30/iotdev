"""OCF exceptions"""

from collections import UserDict
from http import HTTPStatus
import re


class OcfExceptionRegistry(UserDict):
    """Registry of OCF exceptions"""

    def __missing__(self, key):
        """Construct OCF exception class"""
        ns = {'status': key, 'phrase': 'Error %s' % key}
        base = OcfException
        if isinstance(key, int):
            base = self['%dxx' % (key // 100)]
            try:
                # pylint: disable=no-value-for-parameter
                status = HTTPStatus(key)
                ns['phrase'] = status.phrase
                ns['__doc__'] = status.description
            except ValueError:
                pass
        name = 'Ocf%s' % re.sub(r'\W+', '', ns['phrase'])
        return type(name, (base,), ns)


OcfExceptions = OcfExceptionRegistry()


class OcfExceptionMeta(type):
    """OCF exception metaclass"""

    def __call__(cls, *args, **kwargs):
        """Construct exception subclass using callable syntax

        An OCF exception subclass may be constructed using
        `OcfException(status)`, where `status` is the HTTP status
        code.
        """
        if cls.status is None:
            return OcfExceptions[args[0]]
        return super().__call__(cls, *args, **kwargs)


class OcfException(Exception, metaclass=OcfExceptionMeta):
    """OCF exception"""

    status = None
    """HTTP status code

    This is the HTTP status code as defined by RFC 7231.
    """

    phrase = None
    """HTTP reason phrase

    This is the HTTP reason phrase as defined by RFC 7231.
    """

    def __str__(self):
        return self.phrase

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        OcfExceptions[cls.status] = cls


class OcfClientError(OcfException):
    """OCF 4xx Client Error"""

    status = '4xx'
    phrase = 'Client Error'


class OcfServerError(OcfException):
    """OCF 5xx Server Error"""

    status = '5xx'
    phrase = 'Server Error'


OcfBadRequest = OcfException(HTTPStatus.BAD_REQUEST)
OcfUnauthorized = OcfException(HTTPStatus.UNAUTHORIZED)
OcfPaymentRequired = OcfException(HTTPStatus.PAYMENT_REQUIRED)
OcfForbidden = OcfException(HTTPStatus.FORBIDDEN)
OcfNotFound = OcfException(HTTPStatus.NOT_FOUND)
OcfMethodNotAllowed = OcfException(HTTPStatus.METHOD_NOT_ALLOWED)
OcfNotAcceptable = OcfException(HTTPStatus.NOT_ACCEPTABLE)
OcfProxyAuthenticationRequired = OcfException(
    HTTPStatus.PROXY_AUTHENTICATION_REQUIRED
)
OcfRequestTimeout = OcfException(HTTPStatus.REQUEST_TIMEOUT)
OcfConflict = OcfException(HTTPStatus.CONFLICT)
OcfGone = OcfException(HTTPStatus.GONE)
OcfLengthRequired = OcfException(HTTPStatus.LENGTH_REQUIRED)
OcfPreconditionFailed = OcfException(HTTPStatus.PRECONDITION_FAILED)
OcfRequestEntityTooLarge = OcfException(HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
OcfRequestURITooLong = OcfException(HTTPStatus.REQUEST_URI_TOO_LONG)
OcfUnsupportedMediaType = OcfException(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
OcfRequestedRangeNotSatisfiable = OcfException(
    HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
)
OcfExpectationFailed = OcfException(HTTPStatus.EXPECTATION_FAILED)
OcfMisdirectedRequest = OcfException(HTTPStatus.MISDIRECTED_REQUEST)
OcfUnprocessableEntity = OcfException(HTTPStatus.UNPROCESSABLE_ENTITY)
OcfLocked = OcfException(HTTPStatus.LOCKED)
OcfFailedDependency = OcfException(HTTPStatus.FAILED_DEPENDENCY)
OcfUpgradeRequired = OcfException(HTTPStatus.UPGRADE_REQUIRED)
OcfPreconditionRequired = OcfException(HTTPStatus.PRECONDITION_REQUIRED)
OcfTooManyRequests = OcfException(HTTPStatus.TOO_MANY_REQUESTS)
OcfRequestHeaderFieldsTooLarge = OcfException(
    HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE
)

OcfInternalServerError = OcfException(HTTPStatus.INTERNAL_SERVER_ERROR)
OcfNotImplemented = OcfException(HTTPStatus.NOT_IMPLEMENTED)
OcfBadGateway = OcfException(HTTPStatus.BAD_GATEWAY)
OcfServiceUnavailable = OcfException(HTTPStatus.SERVICE_UNAVAILABLE)
OcfGatewayTimeout = OcfException(HTTPStatus.GATEWAY_TIMEOUT)
OcfHTTPVersionNotSupported = OcfException(
    HTTPStatus.HTTP_VERSION_NOT_SUPPORTED
)
OcfVariantAlsoNegotiates = OcfException(HTTPStatus.VARIANT_ALSO_NEGOTIATES)
OcfInsufficientStorage = OcfException(HTTPStatus.INSUFFICIENT_STORAGE)
OcfLoopDetected = OcfException(HTTPStatus.LOOP_DETECTED)
OcfNotExtended = OcfException(HTTPStatus.NOT_EXTENDED)
OcfNetworkAuthenticationRequired = OcfException(
    HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED
)
