# -*- coding: utf-8 -*-
from .. import api
from .. import _


class AbstractCmd(object):
    _name = "AbstractCmd"
    _actions = []

    def __init__(self, action=None, debug=False, **kwargs):
        self._target = None
        self._action = action
        self.debug = debug

    def cmd(self):
        raise NotImplemented

    @property
    def target(self):
        return self._target

    @property
    def action(self):
        action = self._action
        if not action or action not in self._actions:
            action = api.rofi_select(self._actions, title='action:')
        return action

    @property
    def selected_window(self):
        return api.rofi_select_window()

    @property
    def selected_workspace(self):
        return api.rofi_select_workspace()

    @property
    def selected_output(self):
        return api.rofi_select_output()

    def __call__(self, target=None, *args, **kwargs):
        self._target = target
        cmd = self.cmd()
        if not cmd:
            return
        return api.i3_command(cmd, debug=self.debug)


class AbstractWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_window()


class AbstractScratchpadWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.rofi_select_window(scratchpad=True)


class AbstractWorkspaceCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_focused_workspace()


class AbstractBarCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.rofi_select_bar(_('Select bar:'))
