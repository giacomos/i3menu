# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
import mock

from . import MOCK_WINDOW1
from . import MOCK_WINDOW2
from . import MOCK_WINDOW3
from . import MOCK_WINDOWS_LIST
from . import MOCK_WORKSPACES_LIST

from i3menu.connector import I3Connector
from i3menu.menus import AbstractMenu
from i3menu.utils import select
from i3menu.utils import menu
from i3menu.utils import select_window


class TestMenus(unittest.TestCase):

    def setUp(self):
        with mock.patch.object(I3Connector, 'get_windows') as patch:
            patch.return_value = MOCK_WINDOWS_LIST
        with mock.patch.object(I3Connector, 'get_workspaces') as patch:
            patch.return_value = MOCK_WORKSPACES_LIST
        with mock.patch.object(I3Connector, 'get_scratchpad_windows') as patch:
            patch.return_value = MOCK_WINDOWS_LIST

    def tearDown(self):
        pass

    def test_base_menu(self):
        menu = AbstractMenu()
        menu()

#    @mock.patch('i3menu.utils.menu')
#    def test_menu(self, mocked_menu):
#        mocked_menu.return_value = 'Mocked This Silly'
#        ret = menu({'a': [1,2], 'b': [3,4]})
#        self.assertEqual(ret, 'Mocked This Silly')
#
#    @mock.patch('i3menu.utils.menu')
#    def test_select(self, mocked_menu):
#        mocked_menu.return_value = ['x', 'y']
#        options = {'a': ['x', 'y'], 'b': ['w', 'z']}
#        ret = select(options)
#        self.assertEqual(ret, ['x', 'y'])
#
#    @mock.patch('i3menu.utils.menu')
#    def test_select_window(self, mocked_menu):
#        mocked_menu.return_value = MOCK_WINDOW2
#        ret = select_window()
#        self.assertEqual(
#            ret.window_instance, MOCK_WINDOW2.window_instance)
#        # test filter_fnc
#        mocked_menu.return_value = MOCK_WINDOW3
#        filter_fnc = lambda x: x.window_instance == 'mockwindow3'
#        ret = select_window(filter_fnc=filter_fnc)
#        self.assertEqual(
#            ret.window_instance, MOCK_WINDOW3.window_instance)
#        # test when just 1 window is passed
#        mocked_menu.return_value = MOCK_WINDOWS_LIST[0]
#        ret = select_window()
#        self.assertEqual(
#            ret.window_instance, MOCK_WINDOWS_LIST[0].window_instance)
#        # test scratchpad windows
#        mocked_menu.return_value = MOCK_WINDOW1
#        ret = select_window(scratchpad=True)
#        self.assertEqual(
#            ret.window_instance, MOCK_WINDOW1.window_instance)
