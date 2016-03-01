# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    import unittest2 as unittest
except:
    import unittest
from i3menu.menus import AbstractMenu
from i3menu.menus import MenuWindowActions


class TestMenus(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base_menu(self):
        menu = AbstractMenu(config={})
        menu()

    # def test_menu_window_actions(self):
    #     menu = MenuWindowActions(config={})
    #     menu()
