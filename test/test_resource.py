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
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertEqual(self.fridge.prop.n, 'my_fridge')
        self.assertEqual(self.fridge.prop['n'], 'my_fridge')
        self.fridge.prop.n = 'your_fridge'
        self.assertEqual(self.fridge.prop.n, 'your_fridge')
        self.assertEqual(self.fridge.prop['n'], 'your_fridge')
        self.assertEqual(self.fridge['n'], 'your_fridge')

    def test_modify_type(self):
        """Test ability to modify resource type via `rt` property"""
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertNotIsInstance(self.fridge.prop, BinarySwitch)
        self.assertTrue(hasattr(self.fridge.prop, 'defrost'))
        self.assertFalse(hasattr(self.fridge.prop, 'value'))
        self.fridge.prop.rt = ['oic.r.switch.binary']
        self.assertNotIsInstance(self.fridge.prop, Refrigeration)
        self.assertIsInstance(self.fridge.prop, BinarySwitch)
        self.assertFalse(hasattr(self.fridge.prop, 'defrost'))
        self.assertTrue(hasattr(self.fridge.prop, 'value'))

    def test_multi_type(self):
        """Test multi-valued `rt` property"""
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertNotIsInstance(self.fridge.prop, BinarySwitch)
        self.fridge.prop.rt = ['oic.r.refrigeration', 'oic.r.switch.binary']
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertIsInstance(self.fridge.prop, BinarySwitch)
        self.assertTrue(hasattr(self.fridge.prop, 'defrost'))
        self.assertTrue(hasattr(self.fridge.prop, 'value'))

    def test_interface(self):
        """Test accessing resource via interface"""
        self.assertIn('oic.if.baseline', self.fridge.intf)
        baseline = self.fridge.intf['oic.if.baseline'].retrieve()
        self.assertEqual(baseline['filter'], 99)
        self.assertIn('rt', baseline)
        rw = self.fridge.intf['oic.if.rw'].retrieve()
        self.assertIn('n', rw)
        self.assertNotIn('rt', rw)
        self.fridge.intf['oic.if.a'].update({
            'rapidFreeze': True,
            'n': 'ignored_name',
        })
        self.assertTrue(self.fridge.prop.rapidFreeze)
        self.assertEqual(self.fridge.prop.n, 'my_fridge')
