# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
import mock

from . import MOCK_WINDOW1
from . import MOCK_WORKSPACE1

from i3menu.commands import base

from i3menu import menus


class TestMenus(unittest.TestCase):

    def setUp(self):
        with mock.patch.object(
                base.AbstractWindowCmd, 'get_target_window') as patch:
            patch.return_value = MOCK_WINDOW1
        with mock.patch.object(
                base.AbstractWorkspaceCmd, 'get_target_workspace') as patch:
            patch.return_value = MOCK_WORKSPACE1
        with mock.patch.object(
                base.AbstractCmd, 'get_workspace') as patch:
            patch.return_value = MOCK_WORKSPACE1

    def tearDown(self):
        pass

    def test_menu_window_actions(self):
        menu = menus.MenuWindowActions()
        for e in menu._entries:
            option = e['callback']
            with mock.patch('i3menu.utils.menu') as mocked_menu:
                mocked_menu.return_value = option
                ret = menu.select_entry()
            self.assertEqual(ret, option)

    def test_menu_target_window_actions(self):
        menu = menus.MenuTargetWindowActions()
        for e in menu._entries:
            option = e['callback']
            with mock.patch('i3menu.utils.menu') as mocked_menu:
                mocked_menu.return_value = option
                ret = menu.select_entry()
            with mock.patch('i3menu.utils.menu') as mocked_menu:
                mocked_menu.return_value = option
                ret = menu.select_entry()
            self.assertEqual(ret, option)
