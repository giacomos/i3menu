# -*- coding: utf-8 -*-
from .base import AbstractCmd


class CmdGotoWorkspace(AbstractCmd):

    _name = 'goto_workspace'

    def cmd(self):
        return 'workspace "{name}"'.format(name=self.selected_workspace.name)
