# -*- coding: utf-8 -*-
from i3menu import _
from i3menu.connector import I3Connector
from i3menu.config import DEFAULTS
from i3menu.utils import select
from i3menu.utils import select_window
from i3menu.utils import select_workspace
from i3menu.utils import select_output
from i3menu.utils import select_bar


class AbstractCmd(object):
    """ Abstract command """
    _name = "AbstractCmd"
    _description = ''
    _actions = []

    def __init__(self, config=None):
        if not config:
            config = DEFAULTS
        self.config = config
        self.conn = I3Connector(config=config)
        self._target = config.get('target')

    def cmd(self):
        raise NotImplementedError

    def get_action(self):
        action = self.config.get('action')
        if not action or action not in self._actions:
            options = {a: a for a in self._actions}
            action = select(
                options,
                prompt=self._name + ' - action:',
                config=self.config)
        return action

    def get_window(self):
        return select_window(config=self.config)

    def get_workspace(self):
        return select_workspace(config=self.config)

    def get_output(self):
        return select_output(config=self.config)

    def __call__(self):
        cmd = self.cmd()
        if not cmd:
            return
        return self.conn.command(cmd)


class AbstractWindowCmd(AbstractCmd):

    def get_target_window(self):
        return self._target or self.conn.get_focused_window()


class AbstractScratchpadWindowCmd(AbstractCmd):

    def get_target_scratchpad_window(self):
        return self._target or select_window(
            scratchpad=True, config=self.config)


class AbstractWorkspaceCmd(AbstractCmd):

    def get_target_workspace(self):
        return self._target or self.conn.get_focused_workspace()


class AbstractBarCmd(AbstractCmd):

    def get_target_bar(self):
        return self._target or select_bar(
            _('Select bar:'),
            config=self.config)
