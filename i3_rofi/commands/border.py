# -*- coding: utf-8 -*-
from .base import AbstractCmd


class CmdBorder(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_changing_border_style
    """

    _name = 'border'
    _actions = ['none', 'normal', 'pixel 1', 'pixel 3', 'toggle']

    def cmd(self):
        return 'border {action}'.format(action=self.action)
