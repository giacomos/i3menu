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
        target = self.get_target()
        action = self.get_action()
        return '[id="{id}"] fullscreen {action}'.format(
            id=target.window, action=action)
