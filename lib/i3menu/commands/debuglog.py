# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractCmd


class CmdDebuglog(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_enabling_debug_logging
    """

    _name = 'debuglog'
    _actions = ['on', 'off', 'toggle']

    def cmd(self):
        action = self.get_action()
        return 'debuglog {action}'.format(action=action)
