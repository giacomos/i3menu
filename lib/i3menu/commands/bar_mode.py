# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractBarCmd


class CmdBarMode(AbstractBarCmd):
    """ http://i3wm.org/docs/userguide.html#_i3bar_control
    """
    _name = "bar_mode"
    _actions = ['dock', 'hide', 'invisible', 'toggle']

    def cmd(self, action=None):
        target = self.get_target_bar()
        action = self.get_action()
        return 'bar mode {action} "{bar_id}"'.format(
            action=action, bar_id=target)
