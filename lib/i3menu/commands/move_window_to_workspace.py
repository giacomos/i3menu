# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdMoveWindowToWorkspace(AbstractWindowCmd):
    _name = 'move_window_to_workspace'

    def cmd(self, target=None):
        target = self.get_target_window()
        ws = self.get_workspace()
        return '[id="{id}"] move window to workspace "{ws}"'.format(
            id=target.window, ws=ws.name)
