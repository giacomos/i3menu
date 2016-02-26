# -*- coding: utf-8 -*-
from .base import AbstractScratchpadWindowCmd


class CmdScratchpadShow(AbstractScratchpadWindowCmd):
    _name = 'scratchpad_show'

    def cmd(self, target=None):
        return '[id="{id}"] scratchpad show'.format(id=self.target.window)
