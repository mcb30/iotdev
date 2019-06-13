from http import HTTPStatus
from unittest import TestCase
from iotdev.ocf.status import (StatusException, Status, StatusCategory,
                               ClientError, BadRequest, NotFound, ServerError,
                               BadGateway)


class TestExceptions(TestCase):

    def test_inheritance(self):
        """Test inheritance graph"""
        self.assertIsInstance(NotFound(), StatusException)
        self.assertIsInstance(NotFound(), ClientError)
        self.assertNotIsInstance(NotFound(), ServerError)
        self.assertIsInstance(BadGateway(), StatusException)
        self.assertIsInstance(BadGateway(), ServerError)
        self.assertNotIsInstance(BadGateway(), ClientError)
        with self.assertRaises(ClientError):
            raise NotFound
        with self.assertRaises(ClientError):
            raise NotFound('Missing file')

    def test_dynamic(self):
        """Test dynamically constructed exception classes"""
        self.assertIs(Status('4.04'), NotFound)
        with self.assertRaises(ClientError):
            raise Status('4.20')
        with self.assertRaises(StatusCategory('8.xx')):
            raise Status('8.05')
