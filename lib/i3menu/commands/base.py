# -*- coding: utf-8 -*-
from i3menu import api
from i3menu import _


class AbstractCmd(object):
    """ Abstract command """
    _name = "AbstractCmd"
    _description = ''
    _actions = []

    def __init__(self, context=None):
        self._target = context.get('target')
        self._action = context.get('action')
        self.context = context

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
            action = api.menu(
                options,
                title=self._name + ' - action:',
                context=self.context)
        return action

    @property
    def selected_window(self):
        return api.select_window(context=self.context)

    @property
    def selected_workspace(self):
        return api.select_workspace(context=self.context)

    @property
    def selected_output(self):
        return api.select_output(context=self.context)

    def __call__(self, target=None):
        self._target = target
        cmd = self.cmd()
        if not cmd:
            return
        return api.i3_command(cmd, context=self.context)


class AbstractWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_window()


class AbstractScratchpadWindowCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.select_window(
            scratchpad=True, context=self.context)


class AbstractWorkspaceCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.i3_get_focused_workspace()


class AbstractBarCmd(AbstractCmd):

    @property
    def target(self):
        return self._target or api.select_bar(
            _('Select bar:'),
            context=self.context)
