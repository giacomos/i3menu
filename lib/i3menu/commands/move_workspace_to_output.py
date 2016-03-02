# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWorkspaceCmd


class CmdMoveWorkspaceToOutput(AbstractWorkspaceCmd):
    """
    http://i3wm.org/docs/userguide.html#_moving_workspaces_to_a_different_screen
    """
    _name = 'move_workspace_to_output'

    def cmd(self, target=None):
        # XXX: it seems that it's not possible to specify a workspace other
        # than the current one. This needs to be investigated further
        out = self.get_output()
        return 'move workspace to output "{output}"'.format(
            output=out.name)
