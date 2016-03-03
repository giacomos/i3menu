# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdKill(AbstractWindowCmd):
    _name = 'kill'

    def cmd(self):
        target = self.get_target_window()
        return '[id="{id}"] kill'.format(id=target.window)
