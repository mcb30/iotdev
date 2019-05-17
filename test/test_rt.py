from unittest import TestCase
from iotdev.ocf.rt import (BinarySwitch, Brightness, Refrigeration,
                           ResourceType, ResourceTypes)


class DoubleInheritance(BinarySwitch, Brightness):
    pass


class TripleInheritance(Refrigeration, DoubleInheritance):
    pass


class TestResourceType(TestCase):

    def assertIsSubclass(self, a, b):
        self.assertTrue(issubclass(a, b),
                        '%r is not a subclass of %r' % (a, b))

    def assertIsMutualSubclass(self, a, b):
        self.assertIsSubclass(a, b)
        self.assertIsSubclass(b, a)

    def test_registry(self):
        """Test named resource type registry"""
        self.assertIn('oic.r.switch.binary', ResourceTypes)
        self.assertIs(ResourceTypes['oic.r.switch.binary'], BinarySwitch)

    def test_to_rt(self):
        """Test calculation of resource type names"""
        self.assertEqual(BinarySwitch.to_rt(), {'oic.r.switch.binary'})
        self.assertEqual(DoubleInheritance.to_rt(),
                         {'oic.r.switch.binary', 'oic.r.light.brightness'})
        self.assertEqual(TripleInheritance.to_rt(),
                         {'oic.r.switch.binary', 'oic.r.light.brightness',
                          'oic.r.refrigeration'})

    def test_from_rt(self):
        """Test type construction from resource type names"""
        ConstructedBinarySwitch = ResourceType.from_rt('oic.r.switch.binary')
        self.assertIs(ConstructedBinarySwitch, BinarySwitch)
        Double = ResourceType.from_rt('oic.r.switch.binary',
                                      'oic.r.light.brightness')
        self.assertEqual(Double.to_rt(),
                         {'oic.r.switch.binary', 'oic.r.light.brightness'})
        self.assertIsSubclass(Double, BinarySwitch)
        self.assertIsSubclass(Double, Brightness)
        self.assertIsMutualSubclass(Double, DoubleInheritance)

    def test_composite(self):
        """Test type composition"""
        Double = BinarySwitch + Brightness
        self.assertEqual(Double.to_rt(),
                         {'oic.r.switch.binary', 'oic.r.light.brightness'})
        self.assertIsSubclass(Double, BinarySwitch)
        self.assertIsSubclass(Double, Brightness)
        self.assertIsMutualSubclass(Double, DoubleInheritance)
        Triple = Double + Refrigeration
        self.assertEqual(Triple.to_rt(),
                         {'oic.r.switch.binary', 'oic.r.light.brightness',
                          'oic.r.refrigeration'})
        self.assertIsSubclass(Triple, BinarySwitch)
        self.assertIsSubclass(Triple, Brightness)
        self.assertIsSubclass(Triple, Refrigeration)
        self.assertIsSubclass(Triple, Double)
        self.assertIsSubclass(Triple, DoubleInheritance)
        self.assertIsMutualSubclass(Triple, TripleInheritance)
        Subtracted = Triple - BinarySwitch
        self.assertEqual(Subtracted.to_rt(),
                         {'oic.r.light.brightness', 'oic.r.refrigeration'})
        self.assertIsSubclass(Subtracted, Brightness)
        self.assertIsSubclass(Subtracted, Refrigeration)
