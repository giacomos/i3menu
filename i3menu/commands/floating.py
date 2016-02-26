# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractWindowCmd


class CmdFloating(AbstractWindowCmd):
    """ To make the current window floating (or tiling again)
        use floating enable respectively floating disable (or floating toggle)
    """

    _name = 'floating'
    _doc_url = 'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] floating {action}'.format(
            id=self.target.window, action=self.action)
