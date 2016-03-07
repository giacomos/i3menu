# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from . import MOCK_WINDOW1
from . import MOCK_WORKSPACE1
from . import MOCK_OUTPUT1
from i3menu.cmds import AbstractCmd
from i3menu.cmds import Param
from i3menu.cmds import FloatingCmd
from i3menu.cmds import MoveWindowToWorkspaceCmd
from i3menu.cmds import MoveWorkspaceToOutputCmd
from i3menu.exceptions import MissingParamException


class TestCommands(unittest.TestCase):

    def test_abstractcmd_params(self):
        cmd = AbstractCmd()
        self.assertEqual(len(cmd.params()), 0)
        self.assertEqual(cmd.cmd(), '')

    def test_param(self):
        param = Param(name='testparam', fnc=None)
        self.assertEqual(param.name, 'testparam')

    def test_missing_params(self):
        cmd = FloatingCmd()
        self.assertEqual(len(cmd.params()), 2)
        self.assertRaises(MissingParamException, cmd.cmd)

    def test_floating(self):
        cmd = FloatingCmd()
        self.assertEqual(len(cmd.params()), 2)
        res = cmd.cmd(target=MOCK_WINDOW1, action='toggle')
        self.assertEqual(res, u'[id="00000000"] floating toggle')

    def test_move_window_to_workspace(self):
        cmd = MoveWindowToWorkspaceCmd()
        self.assertEqual(len(cmd.params()), 2)
        res = cmd.cmd(target=MOCK_WINDOW1, ws=MOCK_WORKSPACE1)
        self.assertEqual(res, u'[id="00000000"] move window to workspace "MockWorkspace1"')  # noqa

    def test_move_workspace_to_output(self):
        cmd = MoveWorkspaceToOutputCmd()
        self.assertEqual(len(cmd.params()), 1)
        res = cmd.cmd(output=MOCK_OUTPUT1)
        self.assertEqual(res, u'move workspace to output "MockOutput1"')
