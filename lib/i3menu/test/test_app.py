# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from i3menu.app import Application
from i3menu.app import menu_tree
from i3menu.app import menu_root
from i3menu.menu import Menu


class TestCommands(unittest.TestCase):

    def test_application_init(self):
        app = Application()
        self.assertEqual(app.__name__, 'i3menu')

    def test_menu_tree(self):
        tree = menu_tree()
        self.assertEqual(tree.name, 'root')
        self.assertTrue(isinstance(tree, Menu))

    def test_menu_root(self):
        tree = menu_tree()
        tree = menu_root(tree, 'not_existent_menu')
        self.assertEqual(tree.name, 'root')
        tree = menu_root(tree, 'window_actions')
        self.assertEqual(tree.name, 'window_actions')
        self.assertTrue(isinstance(tree, Menu))
