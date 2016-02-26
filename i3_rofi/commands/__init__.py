# -*- coding: utf-8 -*-
from .bar_hidden_state import CmdBarHiddenState
from .bar_mode import CmdBarMode
from .floating import CmdFloating
from .fullscreen import CmdFullscreen
from .goto_workspace import CmdGotoWorkspace
from .kill import CmdKill
from .layout import CmdLayout
from .move_window_to_scratchpad import CmdMoveWindowToScratchpad
from .move_window_to_workspace import CmdMoveWindowToWorkspace
from .move_workspace_to_output import CmdMoveWorkspaceToOutput
from .rename_workspace import CmdRenameWorkspace
from .scratchpad_show import CmdScratchpadShow
from .sticky import CmdSticky


def all_commands():
    cmds = [
        CmdBarHiddenState,
        CmdBarMode,
        CmdFloating,
        CmdFullscreen,
        CmdGotoWorkspace,
        CmdKill,
        CmdLayout,
        CmdMoveWindowToScratchpad,
        CmdMoveWindowToWorkspace,
        CmdMoveWorkspaceToOutput,
        CmdRenameWorkspace,
        CmdScratchpadShow,
        CmdSticky,
    ]
    return {cmd._name: cmd for cmd in cmds}
