# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWorkspaceCmd
from i3menu.utils import menu
from i3menu import _


class CmdRenameWorkspace(AbstractWorkspaceCmd):
    _name = 'rename_workspace'

    def cmd(self, target=None):
        # XXX: this need to use the proper wrapper functions
        target = self.get_target_workspace()
        newname = menu(
            [target.name.encode('utf-8')],
            _('Rename workspace:'),
            **{'format': 's'}
        )
        if not newname:
            return None
        return 'rename workspace "{oldname}" to "{newname}"'.format(
            oldname=self.target.name, newname=newname)
