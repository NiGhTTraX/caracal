from caracal.models import Drainer, BatteryModelBase


class TestBatteryModelNoRecharge(BatteryModelBase):
  def __init__(self, cap, recharge):
    super().__init__(cap, recharge)

  def recharge(self, delta):
    pass


class TestBatteryModelLinear(BatteryModelBase):
  def __init__(self, cap, recharge):
    super().__init__(cap, recharge)

  def recharge(self, delta):
    self.current += self.capacity / self.rechargeTime * delta


class TestDrainer(Drainer):
  def __init__(self, name, discharge, period, activations):
    super().__init__(name, discharge, period)
    self._activations = activations

  @property
  def discharge(self):
    self._activations.append(self)
    return self._discharge

