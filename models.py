from abc import ABCMeta, abstractmethod


class Drainer(object):
  def __init__(self, name, discharge, period):
    self._name = name
    self._discharge = discharge
    self._period = period

  @property
  def discharge(self):
    return self._discharge

  @discharge.setter
  def discharge(self, value):
    self._discharge = value

  @property
  def period(self):
    return self._period

  @period.setter
  def period(self, value):
    self._period = value

  def hasAmmo(self):
    return False

  def __str__(self):
    return self._name

  def __lt__(self, other):
    return self._period < other.period


class DrainerWithAmmo(Drainer):
  def __init__(self, name, discharge, period, capacity, reloadTime):
    super().__init__(name, discharge, period)

    self._capacity = capacity
    self._remaining = capacity
    self._reload = reloadTime

  @property
  def discharge(self):
    # Consume ammo.
    self._remaining -= 1

    return self._discharge

  @property
  def period(self):
    # If we're out of charges, then we must reload.
    if not self._remaining:
      self._remaining = self._capacity
      return self._reload

    return self._period

  def hasAmmo(self):
    return True


class BatteryModelBase(metaclass=ABCMeta):
  def __init__(self, capacity, rechargeTime):
    self._cap = capacity
    self._currentCap = capacity
    self._recharge = rechargeTime

  @property
  def current(self):
    return self._currentCap

  @current.setter
  def current(self, value):
    if value > self._cap:
      self._currentCap = self._cap
    else:
      self._currentCap = value

  @property
  def capacity(self):
    return self._cap

  @capacity.setter
  def capacity(self, value):
    self._cap = value

  @property
  def rechargeTime(self):
    return self._recharge

  @rechargeTime.setter
  def rechargeTime(self, value):
    self._recharge = value

  @abstractmethod
  def recharge(self, currentTime, delta):
    ...

