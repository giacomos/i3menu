# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractCmd


class CmdGotoWorkspace(AbstractCmd):

    _name = 'goto_workspace'

    def cmd(self):
        return 'workspace "{name}"'.format(name=self.selected_workspace.name)
