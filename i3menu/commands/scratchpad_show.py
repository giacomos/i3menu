# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractScratchpadWindowCmd


class CmdScratchpadShow(AbstractScratchpadWindowCmd):
    _name = 'scratchpad_show'

    def cmd(self, target=None):
        return '[id="{id}"] scratchpad show'.format(id=self.target.window)
