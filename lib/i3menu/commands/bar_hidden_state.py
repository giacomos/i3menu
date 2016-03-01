# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractBarCmd


class CmdBarHiddenState(AbstractBarCmd):
    """ http://i3wm.org/docs/userguide.html#_i3bar_control
    """
    _name = "bar_hidden_state"
    _actions = ['hide', 'show', 'toggle']

    def cmd(self, action=None):
        target = self.get_target()
        action = self.get_action()
        return 'bar hidden_state {action} "{bar_id}"'.format(
            action=action, bar_id=target)
