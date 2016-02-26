# -*- coding: utf-8 -*-
from .base import AbstractWindowCmd


class CmdMoveWindowToWorkspace(AbstractWindowCmd):
    _name = 'move_window_to_workspace'

    def cmd(self, target=None):
        return '[id="{id}"] move window to workspace "{ws}"'.format(
            id=self.target.window, ws=self.selected_workspace.name)
