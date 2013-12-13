import unittest

from caracal import Caracal
from caracal.models import Drainer
from caracal.tests.utils import TestDrainer, TestBatteryModelLinear


class TestStability(unittest.TestCase):

  def setUp(self):
    self._model = TestBatteryModelLinear(10, 10)
    self._caracal = Caracal(self._model)

  def test_one_module_stable(self):
    self._caracal.modules = [Drainer("test", 2, 2)]
    self.assertEqual(self._caracal.stability(), (True, 10))

  def test_one_module_not_stable(self):
    self._caracal.modules = [Drainer("test", 2, 1)]
    self.assertEqual(self._caracal.stability(), (False, 8))

