# -*- coding: utf-8 -*-
from .base import AbstractBarCmd


class CmdBarHiddenState(AbstractBarCmd):
    """ http://i3wm.org/docs/userguide.html#_i3bar_control
    """
    _name = "bar_hidden_state"
    _actions = ['hide', 'show', 'toggle']

    def cmd(self, action=None):
        return 'bar hidden_state {action} "{bar_id}"'.format(
            action=self.action, bar_id=self.target)
