# -*- coding: utf-8 -*-
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from zope.component import getUtility

from i3menu.test import BaseTestCase
from i3menu.test import(
    MOCK_WINDOWS_LIST, MOCK_WINDOW1, MOCK_WORKSPACE1, MOCK_OUTPUTS_LIST)
from i3menu.utilities import II3Connector


class TestConnector(BaseTestCase):

    def test_get_windows(self):
        conn = getUtility(II3Connector)
        wins = conn.get_windows()
        self.assertEqual(len(wins), len(MOCK_WINDOWS_LIST))

    def test_get_focused_window(self):
        conn = getUtility(II3Connector)
        win = conn.get_focused_window()
        self.assertEqual(win, MOCK_WINDOW1)

    def test_get_focused_workspace(self):
        conn = getUtility(II3Connector)
        ws = conn.get_focused_workspace()
        self.assertEqual(ws, MOCK_WORKSPACE1)

    def test_get_active_outpus(self):
        conn = getUtility(II3Connector)
        outs = conn.get_active_outputs()
        self.assertEqual(len(outs), len(MOCK_OUTPUTS_LIST) - 1)
