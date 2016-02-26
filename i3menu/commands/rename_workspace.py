# -*- coding: utf-8 -*-
from .base import AbstractWorkspaceCmd
from i3menu import api
from i3menu import _


class CmdRenameWorkspace(AbstractWorkspaceCmd):
    _name = 'rename_workspace'

    def cmd(self, target=None):
        newname = api._rofi(
            [self.target.name.encode('utf-8')],
            _('Rename workspace:'),
            **{'format': 's'}
        )
        if not newname:
            return None
        return 'rename workspace "{oldname}" to "{newname}"'.format(
            oldname=self.target.name, newname=newname)
