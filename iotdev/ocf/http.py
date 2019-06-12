"""HTTP mapping"""

from http import HTTPStatus
from . import status
from .message import Create, Retrieve, Update, Delete, Notify
from .transport import Transport


class HttpClientTransport(Transport):
    """An HTTP client transport"""
    # pylint: disable=abstract-method

    METHOD_MAP = {
        Create.method: 'PUT',
        Retrieve.method: 'GET',
        Update.method: 'PUT',
        Delete.method: 'DELETE',
        Notify.method: 'POST',
    }
    """Map from OCF method to HTTP method"""

    ALLOW_PUT = True
    """Allow use of HTTP PUT"""

    STATUS_MAP = {
        HTTPStatus.OK: status.Content,
        HTTPStatus.CREATED: status.Created,
        HTTPStatus.NO_CONTENT: status.Content,
        HTTPStatus.NOT_MODIFIED: status.Valid,
        HTTPStatus.BAD_REQUEST: status.BadRequest,
        HTTPStatus.UNAUTHORIZED: status.Unauthorized,
        HTTPStatus.FORBIDDEN: status.Forbidden,
        HTTPStatus.NOT_FOUND: status.NotFound,
        HTTPStatus.METHOD_NOT_ALLOWED: status.MethodNotAllowed,
        HTTPStatus.NOT_ACCEPTABLE: status.NotAcceptable,
        HTTPStatus.PRECONDITION_FAILED: status.PreconditionFailed,
        HTTPStatus.REQUEST_ENTITY_TOO_LARGE: status.RequestEntityTooLarge,
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE: status.UnsupportedContentFormat,
        HTTPStatus.UNPROCESSABLE_ENTITY: status.UnprocessableEntity,
        HTTPStatus.TOO_MANY_REQUESTS: status.TooManyRequests,
        HTTPStatus.INTERNAL_SERVER_ERROR: status.InternalServerError,
        HTTPStatus.NOT_IMPLEMENTED: status.Unimplemented,
        HTTPStatus.BAD_GATEWAY: status.BadGateway,
        HTTPStatus.SERVICE_UNAVAILABLE: status.ServiceUnavailable,
        HTTPStatus.GATEWAY_TIMEOUT: status.GatewayTimeout,
    }
    """Map from HTTP status to OCF status"""

    @classmethod
    def method(cls, request):
        """Construct HTTP method from OCF method"""
        res = cls.METHOD_MAP[request.method]
        if res == 'PUT' and not cls.ALLOW_PUT:
            res = 'POST'
        return res

    @classmethod
    def status(cls, stat, request=Retrieve):
        """Construct OCF status from HTTP status code"""
        res = cls.STATUS_MAP.get(stat)
        if res is None:
            res = status.Status('%d.00' % (stat // 100))
        if res.success:
            res = request.success
        return res


class HttpServerTransport(Transport):
    """An HTTP server transport"""
    # pylint: disable=abstract-method

    STATUS_MAP = {
        status.Created: HTTPStatus.CREATED,
        status.Deleted: HTTPStatus.NO_CONTENT,
        status.Valid: HTTPStatus.NOT_MODIFIED,
        status.Changed: HTTPStatus.NO_CONTENT,
        status.Content: HTTPStatus.OK,
        status.BadRequest: HTTPStatus.BAD_REQUEST,
        status.Unauthorized: HTTPStatus.UNAUTHORIZED,
        status.BadOption: HTTPStatus.BAD_REQUEST,
        status.Forbidden: HTTPStatus.FORBIDDEN,
        status.NotFound: HTTPStatus.NOT_FOUND,
        status.MethodNotAllowed: HTTPStatus.BAD_REQUEST,
        status.NotAcceptable: HTTPStatus.NOT_ACCEPTABLE,
        status.PreconditionFailed: HTTPStatus.PRECONDITION_FAILED,
        status.RequestEntityTooLarge: HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        status.UnsupportedContentFormat: HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        status.UnprocessableEntity: HTTPStatus.UNPROCESSABLE_ENTITY,
        status.TooManyRequests: HTTPStatus.TOO_MANY_REQUESTS,
        status.InternalServerError: HTTPStatus.INTERNAL_SERVER_ERROR,
        status.Unimplemented: HTTPStatus.NOT_IMPLEMENTED,
        status.BadGateway: HTTPStatus.BAD_GATEWAY,
        status.ServiceUnavailable: HTTPStatus.SERVICE_UNAVAILABLE,
        status.GatewayTimeout: HTTPStatus.GATEWAY_TIMEOUT,
        status.ProxyingNotSupported: HTTPStatus.BAD_GATEWAY,
    }

    STATUS_NO_CONTENT = {HTTPStatus.NO_CONTENT, HTTPStatus.NOT_MODIFIED}

    @classmethod
    def status(cls, stat, content=None):
        """Construct HTTP status code from OCF status"""
        res = cls.STATUS_MAP.get(stat)
        if res is None:
            # pylint: disable=no-value-for-parameter
            res = HTTPStatus(stat.major * 100)
        if content and res in cls.STATUS_NO_CONTENT:
            res = HTTPStatus.OK
        return res
