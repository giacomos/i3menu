# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    import unittest2 as unittest
except:
    import unittest
from i3menu.utils import which
from i3menu.utils import iteritems
from i3menu.utils import itervalues


class TestUtils(unittest.TestCase):

    def test_which(self):
        self.assertEqual(which('sh'), '/bin/sh')
        self.assertEqual(which('/bin/sh'), '/bin/sh')
        self.assertIsNone(which('dummy_non_existent_programm'))

    def test_iteritems(self):
        pass
