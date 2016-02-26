# -*- coding: utf-8 -*-
from i3menu import api
from i3menu import _


class AbstractCmd(object):
    """ Abstract command """
    _name = "AbstractCmd"
    _description = ''
    _actions = []

    def __init__(self, action=None, **kwargs):
        self._target = None
        self._action = action

    def cmd(self):
        raise NotImplemented

    @property
    def target(self):
        return self._target

    @property
    def action(self):
        action = self._action
        if not action or action not in self._actions:
            options = {a: a for a in self._actions}
            action = api.menu(options, title=self._name + ' - action:')
        return action

    @property
    def selected_window(self):
        return api.select_window()

    @property
    def selected_workspace(self):
        return api.select_workspace()

    @property
    def selected_output(self):
        return api.select_output()

    def __call__(self, target=None, debug=False, *args, **kwargs):
        self._target = target
        cmd = self.cmd()
        if not cmd:
            return
        return api.i3_command(cmd, debug=debug)


class AbstractWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_window()


class AbstractScratchpadWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.select_window(scratchpad=True)


class AbstractWorkspaceCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_focused_workspace()


class AbstractBarCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.select_bar(_('Select bar:'))
