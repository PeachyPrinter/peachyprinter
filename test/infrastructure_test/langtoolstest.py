import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..',))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.langtools import _


class TestGetText(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
