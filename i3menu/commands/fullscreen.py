# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdFullscreen(AbstractWindowCmd):
    """ To make the current window (!) fullscreen, use
        fullscreen enable (or fullscreen enable global for the global mode), to
        leave either fullscreen mode use fullscreen disable, and to toggle between
        these two states use fullscreen toggle (or fullscreen toggle global).
    """

    _name = 'fullscreen'
    _doc_url = 'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] fullscreen {action}'.format(
            id=self.target.window, action=self.action)
