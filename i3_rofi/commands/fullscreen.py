# -*- coding: utf-8 -*-
from .base import AbstractWindowCmd


class CmdFullscreen(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_manipulating_layout
    """

    _name = 'fullscreen'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] fullscreen {action}'.format(
            id=self.target.window, action=self.action)
