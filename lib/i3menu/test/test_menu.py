# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from i3menu.menu import Menu
from i3menu.menu import MenuEntry


class TestMenu(unittest.TestCase):

    def test_menu(self):
        menu = Menu('test', prompt='Dummy')
        self.assertEqual(menu.entries, [])

    def test_menu_parent(self):
        menu = Menu('test')
        menu.parent = True
        self.assertEqual(len(menu.entries), 1)
        self.assertEqual(menu.entries[0].label, '<go back>')

    def test_menu_entries(self):
        entry = MenuEntry(value='dummy_entry', label="DummyEntry")
        menu = Menu('test', entries=[entry])
        self.assertEqual(len(menu.entries), 1)
        self.assertEqual(menu.entries[0].value, 'dummy_entry')
        menu.add_command(label='dummy_entry2', command="dummy")
        self.assertEqual(len(menu.entries), 2)
        submenu = Menu('submenutest', entries=[entry])
        menu.add_cascade(label='dummy_entry2', menu=submenu)
        self.assertEqual(len(menu.entries), 3)

    def test_menu_repr(self):
        menu = Menu('test')
        self.assertEqual(repr(menu), "<i3menu.menu.Menu object 'test'>")
