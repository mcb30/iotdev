from unittest import TestCase
from uuid import UUID
from iotdev.ocf.resource import Resource
from iotdev.ocf.rt import (Device, BinarySwitch, Brightness, Refrigeration,
                           ResourceType)


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
        self.device = Resource({
            'rt': ['oic.wk.d'],
            'di': '4b2e71c3-7f89-44f1-ba58-c8ed780ce780',
        })

    def test_as_dict(self):
        """Test ability to treat resource state as a dictionary"""
        self.assertEqual(self.fridge.state['n'], 'my_fridge')
        self.assertEqual(len(self.fridge.state), 7)
        self.assertIn('defrost', self.fridge.state)
        self.assertIn(99, self.fridge.state.values())
        self.fridge.state['filter'] = 42
        self.assertIn(42, self.fridge.state.values())

    def test_type(self):
        """Test use of typed resource"""
        self.assertEqual(self.fridge.rt, Refrigeration)
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertEqual(self.fridge.prop.n, 'my_fridge')
        self.assertEqual(self.fridge.prop['n'], 'my_fridge')
        self.fridge.prop.n = 'your_fridge'
        self.assertEqual(self.fridge.prop.n, 'your_fridge')
        self.assertEqual(self.fridge.prop['n'], 'your_fridge')
        self.assertEqual(self.fridge.state['n'], 'your_fridge')
        del self.fridge.prop['n']
        self.assertIsNone(self.fridge.prop.n)
        self.assertIsNone(self.fridge.prop['n'])
        self.assertNotIn('n', self.fridge.state)

    def test_modify_type_via_rt(self):
        """Test ability to modify resource type via `rt` attribute"""
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertNotIsInstance(self.fridge.prop, BinarySwitch)
        self.fridge.rt += BinarySwitch
        self.assertIsInstance(self.fridge.prop, Refrigeration)
        self.assertIsInstance(self.fridge.prop, BinarySwitch)
        self.fridge.rt -= Refrigeration
        self.assertNotIsInstance(self.fridge.prop, Refrigeration)
        self.assertIsInstance(self.fridge.prop, BinarySwitch)
        del self.fridge.rt
        self.assertIsInstance(self.fridge.prop, ResourceType)
        self.fridge.rt += 'oic.r.light.brightness'
        self.assertIsInstance(self.fridge.prop, Brightness)
        self.fridge.rt += 'oic.r.switch.binary'
        self.assertIsInstance(self.fridge.prop, (BinarySwitch + Brightness))
        self.fridge.rt = ['oic.r.refrigeration', 'oic.r.switch.binary']
        self.assertIsInstance(self.fridge.prop, (BinarySwitch + Refrigeration))

    def test_modify_type_via_prop(self):
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

    def test_uuid(self):
        """Test UUID property type"""
        self.assertIsInstance(self.device.prop, Device)
        self.assertIsInstance(self.device.prop.di, UUID)
        self.assertEqual(self.device.prop.di,
                         UUID('4b2e71c3-7f89-44f1-ba58-c8ed780ce780'))
        self.device.prop.di = '60ec327c-3057-4044-8462-2136b2d53c31'
        self.assertEqual(self.device.prop.di,
                         UUID('60ec327c-3057-4044-8462-2136b2d53c31'))
        self.device.prop.di = UUID('6f0398c1-ddc7-443e-bf58-64c4c248f5bf')
        self.assertEqual(self.device.prop.di,
                         UUID('6f0398c1-ddc7-443e-bf58-64c4c248f5bf'))
