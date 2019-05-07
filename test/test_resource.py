from unittest import TestCase
from iotdev.ocf.resource import Resource
from iotdev.ocf.rt import BinarySwitch, Refrigeration


class TestResource(TestCase):

    def setUp(self):
        self.fridge = Resource({
            'defrost': False,
            'filter': 99,
            'if': ['oic.if.baseline', 'oic.if.a'],
            'n': 'my_fridge',
            'rapidCool': True,
            'rapidFreeze': False,
            'rt': ['oic.r.refrigeration'],
        })

    def test_as_dict(self):
        """Test ability to treat resource as a state dictionary"""
        self.assertEqual(self.fridge['n'], 'my_fridge')
        self.assertEqual(len(self.fridge), 7)
        self.assertIn('defrost', self.fridge)
        self.assertIn(99, self.fridge.values())
        self.fridge['filter'] = 42
        self.assertIn(42, self.fridge.values())

    def test_type(self):
        """Test use of typed resource"""
        self.assertTrue(issubclass(self.fridge.type, Refrigeration))
        self.assertIsInstance(self.fridge.r, Refrigeration)
        self.assertEqual(self.fridge.r.n, 'my_fridge')
        self.fridge.r.n = 'your_fridge'
        self.assertEqual(self.fridge.r.n, 'your_fridge')
        self.assertEqual(self.fridge['n'], 'your_fridge')

    def test_modify_type(self):
        """Test ability to modify resource type via `rt` property"""
        self.assertIsInstance(self.fridge.r, Refrigeration)
        self.assertNotIsInstance(self.fridge.r, BinarySwitch)
        self.assertTrue(hasattr(self.fridge.r, 'defrost'))
        self.assertFalse(hasattr(self.fridge.r, 'value'))
        self.fridge.r.rt = ['oic.r.switch.binary']
        self.assertNotIsInstance(self.fridge.r, Refrigeration)
        self.assertIsInstance(self.fridge.r, BinarySwitch)
        self.assertFalse(hasattr(self.fridge.r, 'defrost'))
        self.assertTrue(hasattr(self.fridge.r, 'value'))

    def test_multi_type(self):
        """Test multi-valued `rt` property"""
        self.assertIsInstance(self.fridge.r, Refrigeration)
        self.assertNotIsInstance(self.fridge.r, BinarySwitch)
        self.fridge.r.rt = ['oic.r.refrigeration', 'oic.r.switch.binary']
        self.assertIsInstance(self.fridge.r, Refrigeration)
        self.assertIsInstance(self.fridge.r, BinarySwitch)
        self.assertTrue(hasattr(self.fridge.r, 'defrost'))
        self.assertTrue(hasattr(self.fridge.r, 'value'))
