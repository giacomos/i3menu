# -*- coding: utf-8 -*-
from i3menu.commands.bar_hidden_state import CmdBarHiddenState
from i3menu.commands.bar_mode import CmdBarMode
from i3menu.commands.border import CmdBorder
from i3menu.commands.debuglog import CmdDebuglog
from i3menu.commands.exit import CmdExit
from i3menu.commands.floating import CmdFloating
from i3menu.commands.fullscreen import CmdFullscreen
from i3menu.commands.goto_workspace import CmdGotoWorkspace
from i3menu.commands.kill import CmdKill
from i3menu.commands.layout import CmdLayout
from i3menu.commands.move_window_to_scratchpad import CmdMoveWindowToScratchpad
from i3menu.commands.move_window_to_workspace import CmdMoveWindowToWorkspace
from i3menu.commands.move_workspace_to_output import CmdMoveWorkspaceToOutput
from i3menu.commands.reload import CmdReload
from i3menu.commands.rename_workspace import CmdRenameWorkspace
from i3menu.commands.restart import CmdRestart
from i3menu.commands.scratchpad_show import CmdScratchpadShow
from i3menu.commands.shmlog import CmdShmlog
from i3menu.commands.split import CmdSplit
from i3menu.commands.sticky import CmdSticky


def all_commands():
    cmds = [
        CmdBarHiddenState,
        CmdBarMode,
        CmdBorder,
        CmdDebuglog,
        CmdExit,
        CmdFloating,
        CmdFullscreen,
        CmdGotoWorkspace,
        CmdKill,
        CmdLayout,
        CmdMoveWindowToScratchpad,
        CmdMoveWindowToWorkspace,
        CmdMoveWorkspaceToOutput,
        CmdReload,
        CmdRenameWorkspace,
        CmdRestart,
        CmdScratchpadShow,
        CmdShmlog,
        CmdSplit,
        CmdSticky,
    ]
    return {cmd._name: cmd for cmd in cmds}
