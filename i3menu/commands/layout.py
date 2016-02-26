# -*- coding: utf-8 -*-
from .base import AbstractCmd


class CmdLayout(AbstractCmd):
    """ Use layout toggle split, layout stacking, layout tabbed,
        layout splitv or layout splith to change the current container layout to
        splith/splitv, stacking, tabbed layout, splitv or splith, respectively.
    """

    _name = 'layout'
    _doc_url = 'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    _actions = [
        'default', 'tabbed', 'stacking', 'splitv', 'splith',
        'toggle split', 'toggle all']

    def cmd(self):
        return 'layout {action}'.format(action=self.action)
