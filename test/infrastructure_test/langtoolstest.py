import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..',))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.langtools import _


class TestGetText(unittest.TestCase):

    def test_string(self):
        gb_text = 'en_GB Text'
        us_text = 'en_US Text'
        tlh_text = 'tlh Text'

        text = _('en_GB Text')
        self.assertEquals(gb_text, str(text))

        _.switch_lang('en_US')
        text = _('en_GB Text')
        self.assertEquals(us_text, str(text))

        _.switch_lang('tlh')
        text = _('en_GB Text')
        self.assertEquals(tlh_text, str(text))

if __name__ == '__main__':
    unittest.main()
