# -*- coding: utf-8 -*-
from .base import AbstractCmd


class CmdBorder(AbstractCmd):
    """ To change the border of the current client, you can use border normal
        to use the normal border (including window title), border pixel 1 to
        use a 1-pixel border (no window title) and border none to make the
        client borderless.

        There is also border toggle which will toggle the different border
        styles.
    """

    _name = 'border'
    _description = 'change the border style'
    _doc_url = 'http://i3wm.org/docs/userguide.html#_changing_border_style'
    _actions = ['none', 'normal', 'pixel 1', 'pixel 3', 'toggle']

    def cmd(self):
        return 'border {action}'.format(action=self.action)
