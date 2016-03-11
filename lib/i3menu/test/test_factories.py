# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from i3menu.vocabs import init_vocabs
from i3menu.factories import FocusedWindowFactory, FocusedWorkspaceFactory
from i3menu.test import (
    MOCK_CONTEXT,
    MOCK_WINDOW1,
    MOCK_WORKSPACE1
)


class TestFactories(unittest.TestCase):
    def setUp(self):
        self.context = MOCK_CONTEXT
        init_vocabs(self.context)

    def test_focused_window_factory(self):
        fwf = FocusedWindowFactory()
        win = fwf(self.context)
        self.assertEqual(win, MOCK_WINDOW1)
        win = fwf(self.context, vname='no_existent_vocab')
        self.assertEqual(win, None)

    def test_focused_workspace_factory(self):
        fwf = FocusedWorkspaceFactory()
        ws = fwf(self.context)
        self.assertEqual(ws.workspace, MOCK_WORKSPACE1)
        ws = fwf(self.context, vname='no_existent_vocab')
        self.assertEqual(ws, None)
