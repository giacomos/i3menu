# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
import mock
from . import MOCK_OUTPUT1
from . import MOCK_WINDOWS_LIST
from . import MOCK_WORKSPACES_LIST
from . import MOCK_OUTPUTS_LIST
from i3menu.menu import Menu
from i3menu.menu import MenuEntry
from i3menu.menu import ActionsMenu
from i3menu.menu import WindowsMenu
from i3menu.menu import WorkspacesMenu
from i3menu.menu import OutputsMenu


class TestMenu(unittest.TestCase):

    def test_menu(self):
        menu = Menu('test', prompt='Dummy')
        self.assertEqual(menu.entries, [])

    def test_menu_root(self):
        menu = Menu('test')
        menu.root = True
        self.assertEqual(len(menu.entries), 1)
        self.assertEqual(menu.entries[0].label, '<exit>')

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

    def test_actions_menu(self):
        menu = ActionsMenu('test', actions=['a', 'b'])
        self.assertEqual(len(menu.entries), 2)
        self.assertEqual(menu.entries[0].value, 'a')

    def test_windows_menu(self):
        menu = WindowsMenu('test')
        menu.i3.get_windows = mock.MagicMock(return_value=MOCK_WINDOWS_LIST)
        self.assertEqual(len(menu.entries), 3)
        self.assertEqual(menu.entries[0].value.name, 'MockWindow1')
        menu.filter_fnc = lambda e: e.name == 'MockWindow2'
        self.assertEqual(len(menu.entries), 1)
        self.assertEqual(menu.entries[0].value.name, 'MockWindow2')

    def test_workspaces_menu(self):
        menu = WorkspacesMenu('test')
        menu.i3.get_workspaces = mock.MagicMock(return_value=MOCK_WORKSPACES_LIST)
        self.assertEqual(len(menu.entries), len(MOCK_WORKSPACES_LIST))
        self.assertEqual(menu.entries[0].value.name, 'MockWorkspace1')
        menu.filter_fnc = lambda e: e.name == 'MockWorkspace2'
        self.assertEqual(len(menu.entries), 1)
        self.assertEqual(menu.entries[0].value.name, 'MockWorkspace2')

    def test_outputs_menu(self):
        menu = OutputsMenu('test')
        menu.i3.get_active_outputs = mock.MagicMock(
            return_value=MOCK_OUTPUTS_LIST)
        menu.i3.get_focused_output = mock.MagicMock(
            return_value=MOCK_OUTPUT1)
        # this is due to the addiction of the 4 xrandr directions
        self.assertEqual(len(menu.entries), len(MOCK_OUTPUTS_LIST) + 4)
        self.assertEqual(menu.entries[-1].value.name, 'MockOutput2')
        menu.filter_fnc = lambda e: e.name == 'MockOutput2'
        self.assertEqual(len(menu.entries), 1)
        self.assertEqual(menu.entries[0].value.name, 'MockOutput2')
