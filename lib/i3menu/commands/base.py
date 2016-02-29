# -*- coding: utf-8 -*-
from i3menu import api
from i3menu import _


class AbstractCmd(object):
    """ Abstract command """
    _name = "AbstractCmd"
    _description = ''
    _actions = []

    def __init__(self, config=None):
        self.config = config

    def cmd(self):
        raise NotImplemented

    @property
    def target(self):
        return self.config.get('target')

    @property
    def action(self):
        action = self.config.get('action')
        if not action or action not in self._actions:
            options = {a: a for a in self._actions}
            action = api.select(
                options,
                prompt=self._name + ' - action:',
                config=self.config)
        return action

    @property
    def selected_window(self):
        return api.select_window(config=self.config)

    @property
    def selected_workspace(self):
        return api.select_workspace(config=self.config)

    @property
    def selected_output(self):
        return api.select_output(config=self.config)

    def __call__(self):
        cmd = self.cmd()
        if not cmd:
            return
        return api.i3_command(cmd, config=self.config)


class AbstractWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self.config.get('target') or api.i3_get_window()


class AbstractScratchpadWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self.config.get('target') or api.select_window(
            scratchpad=True, config=self.config)


class AbstractWorkspaceCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_focused_workspace()


class AbstractBarCmd(AbstractCmd):

    @property
    def target(self):
        return self.config.get('target') or api.select_bar(
            _('Select bar:'),
            config=self.config)
