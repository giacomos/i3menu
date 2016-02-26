# -*- coding: utf-8 -*-
from .base import AbstractWindowCmd


class CmdFloating(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_manipulating_layout
    """

    _name = 'floating'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] floating {action}'.format(
            id=self.target.window, action=self.action)
