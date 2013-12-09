import unittest

from caracal import Caracal
from caracal.models import Module
from caracal.tests.utils import TestModule, TestCapModelLinear


class TestStability(unittest.TestCase):

  def setUp(self):
    self._model = TestCapModelLinear(10, 10)
    self._caracal = Caracal(self._model)

  def test_one_module_stable(self):
    self._caracal.modules = [Module("test", 2, 2)]
    self.assertEqual(self._caracal.stability(), (True, 10))

  def test_one_module_not_stable(self):
    self._caracal.modules = [Module("test", 2, 1)]
    self.assertEqual(self._caracal.stability(), (False, 8))

