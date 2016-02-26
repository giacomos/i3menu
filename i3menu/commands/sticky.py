# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdSticky(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_sticky_floating_windows
    """

    _name = 'sticky'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] sticky {action}'.format(
            id=self.target.window, action=self.action)
