# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from i3menu.test import BaseTestCase
from i3menu.app import Application


class TestCommands(BaseTestCase):

    def test_application_init(self):
        app = Application()
        self.assertEqual(app.__name__, 'i3menu')

    def test_build_menu_tree(self):
        app = Application()
        tree = app.build_menu_tree()
        self.assertEqual(len(tree.entries), 3)
