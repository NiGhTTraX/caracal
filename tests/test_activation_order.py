import unittest

from caracal import Caracal
from caracal.tests.utils import TestDrainer, TestBatteryModelNoRecharge


class TestActivationOrder(unittest.TestCase):

  def setUp(self):
    self._model = TestBatteryModelNoRecharge(10, 10)
    self._caracal = Caracal(self._model)

  def test_one_module(self):
    actual = []
    mod = TestDrainer("test", 1, 1, actual)
    self._caracal.modules = [mod]

    expected = [mod] * 10
    self._caracal.stability()
    self.assertListEqual(actual, expected)

  def test_two_modules_that_dont_overlap(self):
    actual = []
    mod1 = TestDrainer("test1", 2.5, 3, actual)
    mod2 = TestDrainer("test2", 2.5, 5, actual)
    self._caracal.modules = [mod1, mod2]

    expected = [mod1, mod2, mod1, mod2]
    self._caracal.stability()
    self.assertListEqual(actual, expected)

  def test_two_modules_with_same_period(self):
    actual = []
    mod1 = TestDrainer("test1", 2.5, 2, actual)
    mod2 = TestDrainer("test2", 2.5, 2, actual)
    self._caracal.modules = [mod1, mod2]

    expected = [mod1, mod2, mod1, mod2]
    self._caracal.stability()
    self.assertListEqual(actual, expected)

  def test_two_modules_that_overlap(self):
    actual = []
    mod1 = TestDrainer("test1", 2, 1, actual)
    mod2 = TestDrainer("test2", 2, 2, actual)
    self._caracal.modules = [mod1, mod2]

    expected = [mod1, mod2, mod1, mod1, mod2]
    self._caracal.stability()
    self.assertListEqual(actual, expected)

