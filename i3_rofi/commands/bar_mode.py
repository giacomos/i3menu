# -*- coding: utf-8 -*-
from .base import AbstractBarCmd


class CmdBarMode(AbstractBarCmd):
    """ http://i3wm.org/docs/userguide.html#_i3bar_control
    """
    _name = "bar_mode"
    _actions = ['dock', 'hide', 'invisible', 'toggle']

    def cmd(self, action=None):
        return 'bar mode {action} "{bar_id}"'.format(
            action=self.action, bar_id=self.target)
