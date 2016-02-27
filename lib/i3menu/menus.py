# -*- coding: utf-8 -*-
from i3menu import _
from i3menu import api
from i3menu import commands


class AbstractMenu(object):
    _entries = []
    _prompt = 'Menu:'
    _target = None

    @property
    def target(self):
        return self._target

    def __init__(self, context=None):
        self.context = context

    def __call__(self):
        options = {i['title']: i['callback']for i in self._entries}
        Command = api.menu(options, _(self._prompt))
        cmd = Command(context=self.context)
        return cmd()


class MenuWindowActions(AbstractMenu):
    _name = 'window_actions'
    _prompt = "Window actions:"
    _entries = [
        {'title': _('Move window to workspace'),
         'callback': commands.CmdMoveWindowToWorkspace},
        {'title': _('Border style'),
         'callback': commands.CmdBorder},
        {'title': _('Split'),
         'callback': commands.CmdSplit},
        {'title': _('Floating (toggle)'),
         'callback': commands.CmdFloating},
        {'title': _('Fullscreen (toggle)'),
         'callback': commands.CmdFullscreen},
        {'title': _('Sticky'),
         'callback': commands.CmdSticky},
        {'title': _('Move to Scratchpad'),
         'callback': commands.CmdMoveWindowToScratchpad},
        {'title': _('Quit'),
         'callback': commands.CmdKill}
    ]


class MenuTargetWindowActions(MenuWindowActions):
    _name = 'target_window_actions'

    @property
    def target(self):
        return api.select_window(
            title=_('Select target window:'),
            context=self.context)


class MenuWorkspaceActions(AbstractMenu):
    _name = 'workspace_actions'
    _prompt = "Workspace actions:"

    _entries = [
        {'title': _('Move workspace to output'),
         'callback': commands.CmdMoveWorkspaceToOutput},
        {'title': _('Rename workspace'),
         'callback': commands.CmdRenameWorkspace},
    ]


class MenuTargetWorkspaceActions(MenuWorkspaceActions):
    _name = 'target_workspace_actions'

    @property
    def target(self):
        return api.select_workspace(
            title=_('Select target workspace:'),
            context=self.context)


class MenuBarActions(AbstractMenu):
    _name = 'bar_actions'
    _prompt = "Bar actions:"

    _entries = [
        {'title': _('hidden_state'),
         'callback': commands.CmdBarHiddenState},
        {'title': _('mode'),
         'callback': commands.CmdBarMode},
    ]


class MenuScratchpadActions(AbstractMenu):
    _name = 'scratchpad_actions'
    _prompt = "Scratchpad actions:"

    _entries = [
        {'title': _('Move window to the scratchpad'),
         'callback': commands.CmdMoveWindowToScratchpad},
        {'title': _('Show window from the scratchpad'),
         'callback': commands.CmdScratchpadShow},
    ]


class MenuGotoActions(AbstractMenu):
    _name = 'goto_actions'
    _prompt = "Go to actions:"

    _entries = [
        {'title': _('Go to workspace'),
         'callback': commands.CmdGotoWorkspace},
    ]


class MenuGlobalActions(AbstractMenu):
    _name = 'global_actions'
    _prompt = "Global actions:"

    _entries = [
        {'title': _('Debug log'),
         'callback': commands.CmdDebuglog},
        {'title': _('Shared memory log'),
         'callback': commands.CmdShmlog},
        {'title': _('Restart i3'),
         'callback': commands.CmdRestart},
        {'title': _('Reload i3'),
         'callback': commands.CmdReload},
        {'title': _('Exit i3'),
         'callback': commands.CmdExit},
    ]


def all_menus():
    menus = [
        MenuBarActions,
        MenuGotoActions,
        MenuGlobalActions,
        MenuTargetWindowActions,
        MenuTargetWorkspaceActions,
        MenuWindowActions,
        MenuWorkspaceActions,
        MenuScratchpadActions
    ]
    return {menu._name: menu for menu in menus}
