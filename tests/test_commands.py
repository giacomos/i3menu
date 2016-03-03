# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from mock import MagicMock
import i3menu
from i3menu.commands.base import AbstractCmd
from i3menu import commands

from . import MOCK_WINDOW1
from . import MOCK_WORKSPACE1
from . import MOCK_OUTPUT1


class TestWindowCommands(unittest.TestCase):

    def test_base_command(self):
        menu = AbstractCmd(config={})
        self.assertRaises(NotImplementedError, menu.cmd)
        self.assertRaises(NotImplementedError, menu)

    def test_floating(self):
        menu = commands.CmdFloating(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] floating {action}'.format(
                    winid=MOCK_WINDOW1.window, action=action))

    def test_fullscreen(self):
        menu = i3menu.commands.CmdFullscreen(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] fullscreen {action}'.format(
                    winid=MOCK_WINDOW1.window, action=action))

    def test_sticky(self):
        menu = i3menu.commands.CmdSticky(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] sticky {action}'.format(
                    winid=MOCK_WINDOW1.window, action=action))

    def test_border(self):
        menu = i3menu.commands.CmdBorder(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] border {action}'.format(
                    winid=MOCK_WINDOW1.window, action=action))

    def test_kill(self):
        menu = i3menu.commands.CmdKill(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        self.assertEqual(
            menu.cmd(),
            '[id="{winid}"] kill'.format(
                winid=MOCK_WINDOW1.window))

    def test_move_window_to_workspace(self):
        menu = i3menu.commands.CmdMoveWindowToWorkspace(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        menu.get_workspace = MagicMock(return_value=MOCK_WORKSPACE1)
        self.assertEqual(
            menu.cmd(), '[id="{id}"] move window to workspace "{name}"'.format(
                id=MOCK_WINDOW1.window, name=MOCK_WORKSPACE1.name))

    def test_move_window_to_scratchpad(self):
        menu = i3menu.commands.CmdMoveWindowToScratchpad(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        self.assertEqual(
            menu.cmd(), '[id="{id}"] move to scratchpad'.format(
                id=MOCK_WINDOW1.window))

    def test_split(self):
        menu = i3menu.commands.CmdSplit(config={})
        menu.get_target_window = MagicMock(return_value=MOCK_WINDOW1)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] split {action}'.format(
                    winid=MOCK_WINDOW1.window, action=action))


class TestWorkspaceCommands(unittest.TestCase):

    def test_move_workspace_to_output(self):
        menu = i3menu.commands.CmdMoveWorkspaceToOutput(config={})
        menu.get_output = MagicMock(return_value=MOCK_OUTPUT1)
        self.assertEqual(
            menu.cmd(), 'move workspace to output "{out}"'.format(
                out=MOCK_OUTPUT1.name))

    def test_layout(self):
        menu = i3menu.commands.CmdLayout(config={})
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'layout {action}'.format(action=action))


class TestGlobalCommands(unittest.TestCase):
    def test_debuglog(self):
        menu = i3menu.commands.CmdDebuglog(config={})
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'debuglog {action}'.format(action=action))

    def test_exit(self):
        menu = i3menu.commands.CmdExit(config={})
        self.assertEqual(menu.cmd(), 'exit')

    def test_reload(self):
        menu = i3menu.commands.CmdReload(config={})
        self.assertEqual(menu.cmd(), 'reload')

    def test_restart(self):
        menu = i3menu.commands.CmdRestart(config={})
        self.assertEqual(menu.cmd(), 'restart')

    def test_shmlog(self):
        menu = i3menu.commands.CmdShmlog(config={})
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'shmlog {action}'.format(action=action))

    def test_goto_workspace(self):
        menu = i3menu.commands.CmdGotoWorkspace(config={})
        menu.get_workspace = MagicMock(return_value=MOCK_WORKSPACE1)
        self.assertEqual(
            menu.cmd(), 'workspace "{name}"'.format(name=MOCK_WORKSPACE1.name))


class TestBarCommands(unittest.TestCase):

    def test_bar_hidden_state(self):
        menu = i3menu.commands.CmdBarHiddenState(config={})
        menu.get_target = MagicMock(return_value='bar-0')
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'bar hidden_state {action} "bar-0"'.format(action=action))

    def test_bar_mode(self):
        menu = i3menu.commands.CmdBarMode(config={})
        menu.get_target = MagicMock(return_value='bar-0')
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'bar mode {action} "bar-0"'.format(action=action))
