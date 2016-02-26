# -*- coding: utf-8 -*-
from .base import AbstractCmd


class CmdLayout(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_manipulating_layout
    """

    _name = 'layout'
    _actions = ['default', 'tabbed', 'stacking', 'splitv', 'splith']

    def cmd(self):
        return 'layout {action}'.format(action=self.action)
