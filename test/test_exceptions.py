from http import HTTPStatus
from unittest import TestCase
from iotdev.ocf.exceptions import (OcfException, OcfClientError, OcfBadRequest,
                                   OcfNotFound, OcfServerError, OcfBadGateway)


class TestExceptions(TestCase):

    def test_inheritance(self):
        """Test inheritance graph"""
        self.assertIsInstance(OcfNotFound(), OcfException)
        self.assertIsInstance(OcfNotFound(), OcfClientError)
        self.assertNotIsInstance(OcfNotFound(), OcfServerError)
        self.assertIsInstance(OcfBadGateway(), OcfException)
        self.assertIsInstance(OcfBadGateway(), OcfServerError)
        self.assertNotIsInstance(OcfBadGateway(), OcfClientError)
        with self.assertRaises(OcfClientError):
            raise OcfNotFound
        with self.assertRaises(OcfClientError):
            raise OcfNotFound('Missing file')

    def test_dynamic(self):
        """Test dynamically constructed exception classes"""
        self.assertIs(OcfException(404), OcfNotFound)
        self.assertIs(OcfException(HTTPStatus.NOT_FOUND), OcfNotFound)
        with self.assertRaises(OcfClientError):
            raise OcfException(451)
        with self.assertRaises(OcfException('8xx')):
            raise OcfException(873)
