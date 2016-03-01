# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdSticky(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_sticky_floating_windows
    """

    _name = 'sticky'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        target = self.get_target()
        action = self.get_action()
        return '[id="{id}"] sticky {action}'.format(
            id=target.window, action=action)
