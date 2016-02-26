# -*- coding: utf-8 -*-
from .base import AbstractWindowCmd


class CmdKill(AbstractWindowCmd):
    _name = 'kill'

    def cmd(self):
        return '[id="{id}"] kill'.format(id=self.target.window)
