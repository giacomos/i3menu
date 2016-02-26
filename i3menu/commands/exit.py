# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractCmd


class CmdExit(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    _name = 'exit'

    def cmd(self):
        return self._name
