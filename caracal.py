import heapq
import logging
logger = logging.getLogger(__name__)


def gcd(a, b):
  """Return greatest common divisor using Euclid's Algorithm."""
  while b:
    a, b = b, a % b
  return a


def lcm(a, b):
  """Return lowest common multiple."""
  return a * b // gcd(a, b)


class Caracal(object):
  """Simulate the charging and discharging behavior of a battery.

  Args:
    model: implementation of CapModelBase.
    modules: a list of ModuleBase implementations.
    precision: how many digits should be considered during calculations.
  """
  def __init__(self, model, modules=None, precision=2):
    self._model = model
    self._modules = modules
    self._precision = precision

  @property
  def modules(self):
    return self._modules

  @modules.setter
  def modules(self, value):
    self._modules = value

  @property
  def model(self):
    return self._model

  @model.setter
  def model(self, value):
    self._model = value

  def __prepare(self, method):
    self._activations = []
    multiplier = 10 ** self._precision
    self._eps = 10 ** (-self._precision)
    logging.debug("Precision is %d", self._precision)
    period = 1

    if method == "fast":
      logging.debug("Preparing fast")

      # Get the smallest period.
      period = int(min(m.period for m in self._modules) * multiplier)

      # Create a pseudo module that will have the period set to the smallest
      # period and the discharge will be the ponderate sum of all discharges.
      pseudomod = Module("pseudomod", 0, period)

      for module in self._modules:
        if module.hasAmmo():
          # Don't combine modules that require ammo.
          heapq.heappush(self._activations, (0, module))
          continue

        # Multiply all activation cycles so they become integers.
        p = int(module.period * multiplier)
        module.period = p

        # Stack the discharges proprotionally.
        pseudomod.discharge += module.discharge * (period / p)

      # Push the single pseudomod, if we have one.
      if pseudomod.discharge:
        heapq.heappush(self._activations, (0, pseudomod))
        logging.debug("pseudomod discharge is %f", pseudomod.discharge)
    elif method == "accurate":
      logging.debug("Preparing accurate")

      for module in self._modules:
        # Multiply all activation cycles so they become integers.
        p = int(module.period * multiplier)
        module.period = p

        # Get the lowest common multiple of all the activation cycles.
        period = lcm(period, p)

        # All modules will activate at the beginning.
        logger.debug("Module '%s' %d %d", module, p, module.discharge)
        heapq.heappush(self._activations, (0, module))

    logger.debug("Common period is %d", period)
    self._common = period
    self._multiplier = multiplier

  def stability(self, method="accurate"):
    self.__prepare(method)

    push = heapq.heapreplace
    pop = min

    lastTime = currentTime = 0
    activations = self._activations
    cycle = self._common

    model = self._model
    cap = lastCap = model.capacity
    eps = self._eps
    multiplier = self._multiplier
    k = 0

    while True:
      logging.debug("Iteration %d curCap=%f lastCap=%f", k, cap, lastCap)
      k += 1

      # Get the module that needs to cycle right now.
      now, module = pop(activations)

      # Update the current time.
      currentTime = now

      if currentTime != lastTime:
        # The capacitor has had time to recharge from the last activation.
        delta = (currentTime - lastTime) / multiplier
        model.recharge(delta)
        cap = model.current
        logging.debug("curCap charged to %f", cap)

        # Did we perform a complete activation cycle of all modules?
        if currentTime == cycle:
          logging.debug("--- cycle ---")
          # Do we have more cap than last time?
          if cap > lastCap or abs(cap - lastCap) < eps:
            # We're stable!
            return (True, cap, lastCap)

          # We're currently not stable, may need to do more cycles.
          cycle += self._common
          lastCap = cap

        lastTime = currentTime

      # Drain the cap.
      model.current -= module.discharge
      cap = model.current
      logging.debug("curCap discharged to %f", cap)

      if cap <= 0:
        # We're not stable!
        return (False, currentTime / multiplier)

      # Queue the module again.
      push(activations, (currentTime + module.period, module))

