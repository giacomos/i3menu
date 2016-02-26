# -*- coding: utf-8 -*-
from .base import AbstractWindowCmd


class CmdSplit(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_splitting_containers
    """

    _name = 'split'
    _actions = ['vertical', 'horizontal']

    def cmd(self):
        return '[id="{id}"] layout {action}'.format(
            id=self.target.window, action=self.action)
