# -*- coding: utf-8 -*-
from . import api
from . import _
from .utils import safe_list_get


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


class CmdLayout(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_manipulating_layout
    """

    _name = 'layout'
    _actions = ['default', 'tabbed', 'stacking', 'splitv', 'splith']

    def cmd(self):
        return 'layout {action}'.format(action=self.action)


class CmdGotoWorkspace(AbstractCmd):

    _name = 'goto_workspace'

    def cmd(self):
        return 'workspace "{name}"'.format(name=self.selected_workspace.name)


class CmdFloating(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_manipulating_layout
    """

    _name = 'floating'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] floating {action}'.format(
            id=self.target.window, action=self.action)


class CmdFullscreen(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_manipulating_layout
    """

    _name = 'fullscreen'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] fullscreen {action}'.format(
            id=self.target.window, action=self.action)


class CmdSticky(AbstractWindowCmd):
    """ http://i3wm.org/docs/userguide.html#_sticky_floating_windows
    """

    _name = 'sticky'
    _actions = ['enable', 'disable', 'toggle']

    def cmd(self):
        return '[id="{id}"] sticky {action}'.format(
            id=self.target.window, action=self.action)


class CmdKill(AbstractWindowCmd):
    _name = 'kill'

    def cmd(self):
        return '[id="{id}"] kill'.format(id=self.target.window)


class CmdMoveWindowToScratchpad(AbstractWindowCmd):
    _name = 'move_window_to_scratchpad'

    def cmd(self, target=None):
        return '[id="{id}"] move to scratchpad'.format(id=self.target.window)


class CmdMoveWindowToWorkspace(AbstractWindowCmd):
    _name = 'move_window_to_workspace'

    def cmd(self, target=None):
        return '[id="{id}"] move window to workspace "{ws}"'.format(
            id=self.target.window, ws=self.selected_workspace.name)


class CmdScratchpadShow(AbstractScratchpadWindowCmd):
    _name = 'scratchpad_show'

    def cmd(self, target=None):
        return '[id="{id}"] scratchpad show'.format(id=self.target.window)


class CmdMoveWorkspaceToOutput(AbstractWorkspaceCmd):
    _name = 'move_workspace_to_output'

    def cmd(self, target=None):
        # XXX: it seems that it's not possible to specify a workspace other
        # than the current one. This needs to be investigated further
        # return 'move workspace "{name}" to output "{output}"'.format(
        #     name=self.target.name, output=self.selected_output.name)
        return 'move workspace to output "{output}"'.format(
            output=self.selected_output.name)


class CmdRenameWorkspace(AbstractWorkspaceCmd):
    _name = 'rename_workspace'

    def cmd(self, target=None):
        newname = api._rofi(
            [self.target.name.encode('utf-8')],
            _('Rename workspace:'),
            **{'format': 's'}
        )
        if not newname:
            return None
        return 'rename workspace "{oldname}" to "{newname}"'.format(
            oldname=self.target.name, newname=newname)


class CmdBarMode(AbstractBarCmd):
    """ http://i3wm.org/docs/userguide.html#_i3bar_control
    """
    _name = "bar_mode"
    _actions = ['dock', 'hide', 'invisible', 'toggle']

    def cmd(self, action=None):
        return 'bar mode {action} "{bar_id}"'.format(
            action=self.action, bar_id=self.target)


class CmdBarHiddenState(AbstractBarCmd):
    """ http://i3wm.org/docs/userguide.html#_i3bar_control
    """
    _name = "bar_hidden_state"
    _actions = ['hide', 'show', 'toggle']

    def cmd(self, action=None):
        return 'bar hidden_state {action} "{bar_id}"'.format(
            action=self.action, bar_id=self.target)


class AbstractMenu(object):
    _entries = []
    _prompt = 'Menu:'
    _target = None

    @property
    def target(self):
        return self._target

    def __call__(self):
        target = self.target
        entries = [
            '%s: %s' % (idx + 1, i['title'])
            for idx, i in enumerate(self._entries)]
        idx = api._rofi(entries, _(self._prompt))
        action = safe_list_get(self._entries, idx, None)
        callback = action['callback']
        return callback(target=target)


class MenuWindowActions(AbstractMenu):
    _name = 'window_actions'
    _entries = [
        {'title': _('Move window to workspace:'),
         'callback': CmdMoveWindowToWorkspace()},
        {'title': _('Floating (toggle)'),
         'callback': CmdFloating(action='toggle')},
        {'title': _('Fullscreen (toggle)'),
         'callback': CmdFullscreen(action='toggle')},
        {'title': _('Sticky'),
         'callback': CmdSticky(action='toggle')},
        {'title': _('Move to Scratchpad'),
         'callback': CmdMoveWindowToScratchpad()},
        {'title': _('Quit'),
         'callback': CmdKill()}
    ]


class MenuTargetWindowActions(MenuWindowActions):
    _name = 'target_window_actions'

    @property
    def target(self):
        return api.rofi_select_window(title=_('Select target window:'))


class MenuWorkspaceActions(AbstractMenu):
    _name = 'workspace_actions'

    _entries = [
        {'title': _('Move workspace to output:'),
         'callback': CmdMoveWorkspaceToOutput()},
        {'title': _('Rename workspace:'),
         'callback': CmdRenameWorkspace()},
    ]


class MenuTargetWorkspaceActions(MenuWorkspaceActions):
    _name = 'target_workspace_actions'

    @property
    def target(self):
        return api.rofi_select_workspace(title=_('Select target workspace:'))


class MenuBarActions(AbstractMenu):
    _name = 'bar_actions'

    _entries = [
        {'title': _('hidden_state'),
         'callback': CmdBarHiddenState()},
        {'title': _('mode'),
         'callback': CmdBarMode()},
    ]


class MenuScratchpadActions(AbstractMenu):
    _name = 'scratchpad_actions'

    _entries = [
        {'title': _('Move window to the scratchpad'),
         'callback': CmdMoveWindowToScratchpad()},
        {'title': _('Show window from the scratchpad'),
         'callback': CmdScratchpadShow()},
    ]


class MenuGotoActions(AbstractMenu):
    _name = 'goto_actions'

    _entries = [
        {'title': _('Go to workspace'),
         'callback': CmdGotoWorkspace()},
    ]


def all_commands():
    cmds = [
        CmdBarHiddenState,
        CmdBarMode,
        CmdFloating,
        CmdFullscreen,
        CmdGotoWorkspace,
        CmdKill,
        CmdLayout,
        CmdMoveWindowToScratchpad,
        CmdMoveWindowToWorkspace,
        CmdMoveWorkspaceToOutput,
        CmdRenameWorkspace,
        CmdScratchpadShow,
        CmdSticky,
    ]
    return {cmd._name: cmd for cmd in cmds}


def all_menus():
    menus = [
        MenuBarActions,
        MenuGotoActions,
        MenuTargetWindowActions,
        MenuTargetWorkspaceActions,
        MenuWindowActions,
        MenuWorkspaceActions,
        MenuScratchpadActions
    ]
    return {menu._name: menu for menu in menus}
