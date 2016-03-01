# -*- coding: utf-8 -*-
from collections import OrderedDict
from i3menu import _
from i3menu.utils import select
from i3menu.utils import select_window
from i3menu.utils import select_workspace
from i3menu import commands
from i3menu.config import DEFAULTS


class AbstractMenu(object):
    _entries = []
    _prompt = 'Menu:'

    def __init__(self, config=None):
        if not config:
            config = DEFAULTS
        self.config = config

    @property
    def target(self):
        return self.config.get('target')

    def __call__(self):
        options = OrderedDict()
        for i in self._entries:
            options[i['title']] = i['callback']
        self.config['target'] = self.target
        Command = select(options, _(self._prompt), config=self.config)
        if not Command:
            return
        cmd = Command(config=self.config)
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
        return select_window(
            prompt=_('Select target window:'), config=self.config
        )


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
        return select_workspace(
            prompt=_('Select target workspace:'), config=self.config
        )


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
