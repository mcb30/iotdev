from json import loads
from unittest import TestCase
from iotdev.ocf.state import ResourceState
from iotdev.ocf.message import Message


class TestMessage(TestCase):

    def test_init_data(self):
        """Test initialisation via data=..."""
        msg1 = Message({'temperature': 23, 'units': 'C'})
        self.assertIsInstance(msg1.state, ResourceState)
        self.assertSetEqual(set(msg1.state), {'temperature', 'units'})
        self.assertEqual(msg1.state['temperature'], 23)
        msg2 = Message(data={'enabled': True})
        self.assertSetEqual(set(msg2.state), {'enabled'})
        self.assertTrue(msg2.state['enabled'])

    def test_init_json(self):
        """Test initialisation via json=..."""
        msg = Message(json='{"temperature": 24}')
        self.assertIsInstance(msg.state, ResourceState)
        self.assertEqual(msg.state['temperature'], 24)

    def test_init_state(self):
        """Test initialisation via state=..."""
        state = ResourceState({'temperature': 21})
        msg = Message(state=state)
        self.assertIs(msg.state, state)
        self.assertEqual(loads(msg.json), {'temperature': 21})
