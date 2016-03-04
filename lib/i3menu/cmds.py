# -*- coding: utf-8 -*-
from i3menu import _
from i3menu.exceptions import MissingParamException
from i3menu.menu import WindowsMenu
from i3menu.menu import WorkspacesMenu
from i3menu.menu import OutputsMenu
from i3menu.menu import ActionsMenu


class AbstractCmd(object):
    """ Abstract command """
    _name = "AbstractCmd"
    _description = ''
    _cmd = ''

    def cmd(self, *args, **kwargs):
        """ make the window/container floating. If not target it provided
            the focused window will be used by default.
        """
        params = self.params()
        for p in params:
            if p.name not in kwargs:
                error = 'Missing required parameter: {p}'.format(p=p.name)
                raise MissingParamException(error)
        return self._cmd.format(**kwargs)

    def params(self):
        res = []
        for base_klass in self.__class__.__bases__:
            if hasattr(base_klass, '_params'):
                res += base_klass._params(self)
        return res


class Param(object):
    name = u'generic'
    fnc = None
    default = None
    default_fnc = None

    def __init__(
            self, name, fnc, default=None, default_fnc=None):
        self.name = name
        self.fnc = fnc
        self.default = default
        self.default_fnc = default_fnc


class AbstractActionCmd(AbstractCmd):
    _actions = []

    @property
    def actions(self):
        return self._actions

    def _params(self):
        params = []
        params.append(
            Param(
                'action',
                ActionsMenu(
                    'action',
                    prompt=_(u"Select action"), actions=self.actions),
                default='toggle' in self._actions and 'toggle' or None
            )
        )
        return params


class AbstractTargetWindowCmd(AbstractCmd):
    def _params(self):
        params = []
        params.append(
            Param(
                'target',
                WindowsMenu(
                    'target', prompt=_(u"Select window")),
                default_fnc=lambda e: e.value.focused
            )
        )
        return params


class AbstractWorkspaceCmd(AbstractCmd):
    def _params(self):
        params = []
        params.append(
            Param(
                'ws',
                WorkspacesMenu('ws', prompt=_(u"Select workspace")),
            )
        )
        return params


class AbstractOutputCmd(AbstractCmd):
    def _params(self):
        params = []
        params.append(
            Param(
                'output',
                OutputsMenu('output', prompt=_(u"Select output")),
            )
        )
        return params


class FloatingCmd(AbstractTargetWindowCmd, AbstractActionCmd):
    """ To make the current window floating (or tiling again)
        use floating enable respectively floating disable (or floating toggle)
    """

    _name = u"floating"
    _doc_url = u"http://i3wm.org/docs/userguide.html#_manipulating_layout"
    _actions = [u"enable", u"disable", u"toggle"]
    _cmd = u"[id='{target.window}'] floating {action}"


class KillCmd(AbstractTargetWindowCmd):
    _name = u"kill"
    _cmd = u"[id='{target.window}'] kill"


class BorderCmd(AbstractTargetWindowCmd, AbstractActionCmd):
    """ To change the border of the current client, you can use border normal
        to use the normal border (including window title), border pixel 1 to
        use a 1-pixel border (no window title) and border none to make the
        client borderless.

        There is also border toggle which will toggle the different border
        styles.
    """

    _name = u"border"
    _description = u"change the border style"
    _doc_url = 'http://i3wm.org/docs/userguide.html#_changing_border_style'
    _actions = ['none', 'normal', 'pixel 1', 'pixel 3', 'toggle']
    _cmd = '[id="{target.window}"] border {action}'


class MoveWindowToScratchpadCmd(AbstractTargetWindowCmd):
    _name = u"move_window_to_scratchpad"
    _cmd = u"[id='{target.window}'] move to scratchpad"


class StickyCmd(AbstractTargetWindowCmd, AbstractActionCmd):
    """ http://i3wm.org/docs/userguide.html#_sticky_floating_windows
    """

    _name = u"sticky"
    _actions = [u"enable", u"disable", u"toggle"]
    _cmd = u"[id='{target.window}'] sticky {action}"


class MoveWindowToWorkspaceCmd(AbstractTargetWindowCmd, AbstractWorkspaceCmd):
    _name = u"move_window_to_workspace"
    _cmd = u"[id='{target.window}'] move window to workspace '{ws.name}'"


class SplitCmd(AbstractTargetWindowCmd, AbstractActionCmd):
    """ http://i3wm.org/docs/userguide.html#_splitting_containers
    """

    _name = u"split"
    _cmd = u"[id='{target.window}'] split {action}"
    _actions = ['vertical', 'horizontal']


class FullscreenCmd(AbstractTargetWindowCmd, AbstractActionCmd):
    """ To make the current window (!) fullscreen, use
        fullscreen enable (or fullscreen enable global for the global mode),
        to leave either fullscreen mode use fullscreen disable, and to toggle
        between these two states use fullscreen toggle (or fullscreen toggle
        global).
    """

    _name = u"fullscreen"
    _cmd = u"[id='{target.window}'] fullscreen {action}"
    _doc_url = 'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    _actions = ['enable', 'disable', 'toggle']


class DebuglogCmd(AbstractActionCmd):
    """ http://i3wm.org/docs/userguide.html#_enabling_debug_logging
    """

    _name = u"debuglog"
    _cmd = u"debuglog {action}"
    _actions = ['on', 'off', 'toggle']


class ShmlogCmd(AbstractActionCmd):
    """ http://i3wm.org/docs/userguide.html#shmlog
    """

    _name = u"shmlog"
    # TODO: add the possibility to specify the shared memory size
    _cmd = u"shmlog {action}"
    _actions = ['on', 'off', 'toggle']


class ReloadCmd(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    _name = u"reload"
    _cmd = u"reload"


class RestartCmd(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    _name = u"restart"
    _cmd = u"restart"


class ExitCmd(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    _name = u"exit"
    _cmd = u"exit"


class GotoWorkspaceCmd(AbstractWorkspaceCmd):

    _name = u"goto_workspace"
    _cmd = u"workspace '{ws.name}'"


class MoveWorkspaceToOutputCmd(AbstractOutputCmd):
    """
    http://i3wm.org/docs/userguide.html#_moving_workspaces_to_a_different_screen
    """
    # XXX: it seems that it's not possible to specify a workspace other
    # than the current one. This needs to be investigated further
    _name = 'move_workspace_to_output'
    _cmd = u"move workspace to output '{output.name}'"


class LayoutCmd(AbstractActionCmd):
    """ Use layout toggle split, layout stacking, layout tabbed,
        layout splitv or layout splith to change the current container layout
        to splith/splitv, stacking, tabbed layout, splitv or splith,
        respectively.
    """

    _name = u"exit"
    _cmd = u"layout {action}"
    _doc_url = 'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    _actions = [
        'default', 'tabbed', 'stacking', 'splitv', 'splith',
        'toggle split', 'toggle all']
