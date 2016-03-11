# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from i3menu.app import Application


class TestCommands(unittest.TestCase):

    def test_application_init(self):
        app = Application()
        self.assertEqual(app.__name__, 'i3menu')
