# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdSplit(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_splitting_containers
    """

    _name = 'split'
    _actions = ['vertical', 'horizontal']

    def cmd(self):
        target = self.get_target_window()
        action = self.get_action()
        return '[id="{id}"] split {action}'.format(
            id=target.window, action=action)
