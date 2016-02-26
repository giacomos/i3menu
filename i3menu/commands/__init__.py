# -*- coding: utf-8 -*-
from .bar_hidden_state import CmdBarHiddenState
from .bar_mode import CmdBarMode
from .border import CmdBorder
from .debuglog import CmdDebuglog
from .exit import CmdExit
from .floating import CmdFloating
from .fullscreen import CmdFullscreen
from .goto_workspace import CmdGotoWorkspace
from .kill import CmdKill
from .layout import CmdLayout
from .move_window_to_scratchpad import CmdMoveWindowToScratchpad
from .move_window_to_workspace import CmdMoveWindowToWorkspace
from .move_workspace_to_output import CmdMoveWorkspaceToOutput
from .reload import CmdReload
from .rename_workspace import CmdRenameWorkspace
from .restart import CmdRestart
from .scratchpad_show import CmdScratchpadShow
from .shmlog import CmdShmlog
from .split import CmdSplit
from .sticky import CmdSticky


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
