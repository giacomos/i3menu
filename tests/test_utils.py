# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from i3menu.utils import which
from i3menu.app import Application


class TestMenus(unittest.TestCase):

    def test_which(self):
        self.assertEqual(which('/bin/sh'), '/bin/sh')
        self.assertEqual(which('sh'), '/bin/sh')
        self.assertIsNone(which('verystupidcommand'))
