# -*- coding: utf-8 -*-
from .base import AbstractWindowCmd


class CmdMoveWindowToScratchpad(AbstractWindowCmd):
    _name = 'move_window_to_scratchpad'

    def cmd(self, target=None):
        return '[id="{id}"] move to scratchpad'.format(id=self.target.window)
