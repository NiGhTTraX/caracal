#!/usr/bin/env python3

import os
import sys
import unittest


if __name__ == "__main__":
  # Add the caracal package to the python path.
  scriptDir = os.path.dirname(os.path.abspath(__file__))
  sys.path.append(os.path.realpath(os.path.join(scriptDir, '..', '..')))

  # Discover tests and run them.
  tests = unittest.TestLoader().discover(scriptDir, 'test_*.py')
  unittest.TextTestRunner().run(tests)

