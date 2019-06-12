"""Transport using `requests` library"""

import cgi
from urllib.parse import urljoin
import requests
from ..ocf.message import Response
from ..ocf.transport import Transports
from ..ocf.http import HttpClientTransport

class RequestsTransport(HttpClientTransport):
    """Transport using `requests` library"""

    schemes = ('http', 'https')

    def __init__(self):
        self.session = requests.Session()

    def request(self, ep, msg):
        """Construct HTTP request"""
        method = self.method(msg)
        uri = urljoin(ep.uri, msg.uri)
        headers = {'Accept': 'application/json'}
        if msg.state:
            headers['Content-Type'] = 'application/json'
        req = requests.Request(method, uri, headers=headers, data=msg.json,
                               params=msg.params.items())
        return self.session.prepare_request(req)

    def response(self, rsp, req):
        """Construct OCF response"""
        status = self.status(rsp.status_code, req)
        mimetype, _ = cgi.parse_header(rsp.headers.get('Content-Type', ''))
        json = rsp.text if mimetype == 'application/json' else None
        return Response(status, json=json)

    def dispatch(self, ep, msg):
        return self.response(self.session.send(self.request(ep, msg)), msg)


Transports.register(RequestsTransport())
