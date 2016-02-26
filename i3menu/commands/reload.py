# -*- coding: utf-8 -*-
from .base import AbstractCmd


class CmdReload(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    _name = 'reload'

    def cmd(self):
        return self._name
