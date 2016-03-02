# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from i3menu.commands.base import AbstractCmd
from i3menu import commands

from mock import MagicMock
try:
    import unittest2 as unittest
except:
    import unittest


class DummyWindow(object):
    window = 12345678


class DummyWorkspace(object):
    name = 'dummy'


class DummyOutput(object):
    name = 'dummy'


dummy_window = DummyWindow()
dummy_workspace = DummyWorkspace()
dummy_output = DummyOutput()


class TestWindowCommands(unittest.TestCase):

    def test_base_command(self):
        menu = AbstractCmd(config={})
        self.assertRaises(NotImplementedError, menu.cmd)
        self.assertRaises(NotImplementedError, menu)

    def test_floating(self):
        menu = commands.CmdFloating(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] floating {action}'.format(
                    winid=dummy_window.window, action=action))

    def test_fullscreen(self):
        menu = commands.CmdFullscreen(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] fullscreen {action}'.format(
                    winid=dummy_window.window, action=action))

    def test_sticky(self):
        menu = commands.CmdSticky(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] sticky {action}'.format(
                    winid=dummy_window.window, action=action))

    def test_border(self):
        menu = commands.CmdBorder(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] border {action}'.format(
                    winid=dummy_window.window, action=action))

    def test_kill(self):
        menu = commands.CmdKill(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        self.assertEqual(
            menu.cmd(),
            '[id="{winid}"] kill'.format(
                winid=dummy_window.window))

    def test_move_window_to_workspace(self):
        menu = commands.CmdMoveWindowToWorkspace(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        menu.get_workspace = MagicMock(return_value=dummy_workspace)
        self.assertEqual(
            menu.cmd(), '[id="{id}"] move window to workspace "{name}"'.format(
                id=dummy_window.window, name=dummy_workspace.name))

    def test_move_window_to_scratchpad(self):
        menu = commands.CmdMoveWindowToScratchpad(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        self.assertEqual(
            menu.cmd(), '[id="{id}"] move to scratchpad'.format(
                id=dummy_window.window))

    def test_split(self):
        menu = commands.CmdSplit(config={})
        menu.get_target = MagicMock(return_value=dummy_window)
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                '[id="{winid}"] split {action}'.format(
                    winid=dummy_window.window, action=action))


class TestWorkspaceCommands(unittest.TestCase):

    def test_move_workspace_to_output(self):
        menu = commands.CmdMoveWorkspaceToOutput(config={})
        menu.get_output = MagicMock(return_value=dummy_output)
        self.assertEqual(
            menu.cmd(), 'move workspace to output "{out}"'.format(
                out=dummy_output.name))

    def test_layout(self):
        menu = commands.CmdLayout(config={})
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'layout {action}'.format(action=action))


class TestGlobalCommands(unittest.TestCase):
    def test_debuglog(self):
        menu = commands.CmdDebuglog(config={})
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'debuglog {action}'.format(action=action))

    def test_exit(self):
        menu = commands.CmdExit(config={})
        self.assertEqual(menu.cmd(), 'exit')

    def test_reload(self):
        menu = commands.CmdReload(config={})
        self.assertEqual(menu.cmd(), 'reload')

    def test_restart(self):
        menu = commands.CmdRestart(config={})
        self.assertEqual(menu.cmd(), 'restart')

    def test_shmlog(self):
        menu = commands.CmdShmlog(config={})
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'shmlog {action}'.format(action=action))

    def test_goto_workspace(self):
        menu = commands.CmdGotoWorkspace(config={})
        menu.get_workspace = MagicMock(return_value=dummy_workspace)
        self.assertEqual(
            menu.cmd(), 'workspace "{name}"'.format(name=dummy_workspace.name))


class TestBarCommands(unittest.TestCase):

    def test_bar_hidden_state(self):
        menu = commands.CmdBarHiddenState(config={})
        menu.get_target = MagicMock(return_value='bar-0')
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'bar hidden_state {action} "bar-0"'.format(action=action))

    def test_bar_mode(self):
        menu = commands.CmdBarMode(config={})
        menu.get_target = MagicMock(return_value='bar-0')
        for action in menu._actions:
            menu.get_action = MagicMock(return_value=action)
            self.assertEqual(
                menu.cmd(),
                'bar mode {action} "bar-0"'.format(action=action))
