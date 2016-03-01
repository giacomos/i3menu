# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdMoveWindowToScratchpad(AbstractWindowCmd):
    _name = 'move_window_to_scratchpad'

    def cmd(self, target=None):
        target = self.get_target()
        return '[id="{id}"] move to scratchpad'.format(id=target.window)
