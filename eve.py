from models import CapModelBase

from math import sqrt
import numpy as np


# Hyperbolic secant function.
sech = lambda x: 2 / (np.exp(x) + np.exp(-x))

# Inverse hyperbolic secant function.
arcsech = lambda x: np.arccosh(1 / x)


class CapModel(CapModelBase):
  """Recharge cap using DustPuppy's original equation."""
  def __init__(self, cap, recharge):
    super().__init__(cap, recharge)

  def recharge(self, delta):
    C = self._cap
    c = self._currentCap
    tau = self._recharge / 5

    self._currentCap = C * (1 + (sqrt(c / C) - 1) * np.exp(-delta / tau))**2


class CapModelInverse(CapModelBase):
  """Recharge cap by solving for t in capacitor over time equation and then
  solving the same equation for cap substituting t with t + delta."""
  def __init__(self, cap, recharge):
    super().__init__(cap, recharge)

  def recharge(self, delta):
    C = self._cap
    c = self._currentCap
    tau = 5 / self._recharge

    # Solve time for current capacity
    t = 1 / tau * arcsech((C - c) / C)

    self.current = C * (1 - 1 / (np.cosh(tau * (t + delta))))


class CapModelRecharge(CapModelBase):
  """Recharge cap by solving for t in capacitor over time equation and then
  adding the integral of the recharge over time equation from t to t + delta."""
  def __init__(self, cap, recharge):
    super().__init__(cap, recharge)

  def recharge(self, delta):
    C = self._cap
    c = self._currentCap
    tau = 5 / self._recharge

    # Solve time for current capacity
    t = 1 / tau * arcsech((C - c) / C)

    rfunc = lambda tau, C, t: -C * sech(tau * t)
    self.current += rfunc(tau, C, t + delta) - rfunc(tau, C, t)


class CapModelLinear(CapModelBase):
  """Linear recharge model."""
  def __init__(self, cap, recharge):
    super().__init__(cap, recharge)

  def recharge(self, delta):
    self.current += self._cap / self._recharge * delta

