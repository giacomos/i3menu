from zope.interface import implementer, providedBy
from zope.component import getAdapter, getGlobalSiteManager
from zope.component import getUtility


from i3menu import _
from i3menu import logger
from i3menu import interfaces
from i3menu.menu import Menu
from i3menu.interfaces import II3Connector
from i3menu.exceptions import MissingParamException
from past.builtins import basestring

gsm = getGlobalSiteManager()


class AbstractCmd(object):
    """ Abstract command """
    __id__ = u'AbstractCmd'
    __title__ = _(u'Abstract Command')
    __url__ = u''
    __cmd__ = u''

    def __init__(self, context):
        self.context = context
        self.params = [p for p in self._get_params()]
        self.data = self.get_defaults()

    def get_defaults(self):
        defaults = {}
        for pname, param in self.params:
            param.context = self.context
            param.bind(self.context)
            if param.default:
                defaults[pname] = param.default
        return defaults

    def validate_data(self):
        allparams = self.paramsdict()
        for pname in allparams:
            if pname not in self.data:
                logger.info('Missing parameter: %s' % pname)
                return False
        return True

    def __call__(self):
        cmd_msg = None
        self.request_params()
        cmd_msg = self.cmd(**self.data)
        if cmd_msg:
            conn = getUtility(II3Connector)
            logger.debug('Run command: {cmd}'.format(cmd=cmd_msg))
            return conn.command(cmd_msg)

    def cmd(self, *args, **kwargs):
        params = kwargs.copy()
        allparams = self.paramsdict()
        for pname in allparams:
            if pname not in params:
                if allparams[pname].default:
                    params[pname] = allparams[pname].default
                else:
                    error = u'Missing required parameter: {p}'.format(p=pname)
                    raise MissingParamException(error)
        return self.__cmd__.format(**params)

    def _get_params(self):
        interfaces = [i for i in providedBy(self).interfaces()]
        for i in interfaces:
            fields = [(fname, field)
                      for fname, field in i.namesAndDescriptions()]
            fields = sorted(fields, key=lambda f: f[1].order)
            for fname, field in fields:
                yield fname, field

    def paramsdict(self):
        res = {pname: p for pname, p in self.params}
        return res

    def _missing_params(self):
        return [
            (fname, field)
            for fname, field in self.params if fname not in self.data]

    def _present_params(self):
        return [
            (fname, field)
            for fname, field in self.params if fname in self.data]

    def params_summary_menu(self):
        params_menu = Menu(u'params_menu', prompt=self.__title__)
        if self.validate_data():
            params_menu.add_command(label='Run!', command='run')
        missing_params = self._missing_params()
        present_params = self._present_params()
        for fname, field in missing_params + present_params:
            field.bind(self.context)
            widget = getAdapter(field, interfaces.IWidget)
            current_value = 'N/A'
            if fname in self.data:
                val = self.data[fname]
                if isinstance(val, basestring):
                    current_value = val
                else:
                    current_value = val.name
            label = u'{name} = {value}'.format(
                name=fname, value=current_value)
            entry = params_menu.add_command(
                label=label,
                command=widget)
            entry.name = fname
        return self.context.selectinput(params_menu)

    def param_menu(self, name, widget):
        newvalue = widget()
        if newvalue:
            self.data[name] = newvalue

    def request_params(self):
        res = self.params_summary_menu()
        if not res or res.value == 'run':
            return
        elif interfaces.IWidget.providedBy(res.value):
            self.param_menu(res.name, res.value)
        self.request_params()


@implementer(interfaces.IFloating)
class Floating(AbstractCmd):
    __id__ = u'floating'
    __title__ = _(u'Floating')
    __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    __cmd__ = u'[id="{window.window}"] floating {action}'


gsm.registerUtility(
    Floating,
    interfaces.IFloating,
    name=Floating.__id__)


@implementer(interfaces.IMoveWindowToWorkspace)
class MoveWindowToWorkspace(AbstractCmd):
    __id__ = u'move_window_to_workspace'
    __title__ = _(u'Move Window To Workspace')
    __cmd__ = u'[id="{window.window}"] move window to workspace '\
        '"{workspace.workspace.name}"'


gsm.registerUtility(
    MoveWindowToWorkspace,
    interfaces.IMoveWindowToWorkspace,
    name=MoveWindowToWorkspace.__id__)


@implementer(interfaces.IMoveWorkspaceToOutput)
class MoveWorkspaceToOutput(AbstractCmd):
    """
    http://i3wm.org/docs/userguide.html#_moving_workspaces_to_a_different_screen
    """
    # XXX: it seems that it's not possible to specify a workspace other
    # than the current one. This needs to be investigated further
    __id__ = u'move_workspace_to_output'
    __title__ = u'Move Workspace To Output'
    __cmd__ = u'move workspace to output "{output.output.name}"'


gsm.registerUtility(
    MoveWorkspaceToOutput,
    interfaces.IMoveWorkspaceToOutput,
    MoveWorkspaceToOutput.__id__)


@implementer(interfaces.IRenameWorkspace)
class RenameWorkspace(AbstractCmd):
    __id__ = u'rename'
    __title__ = u'Rename workspace'
    __cmd__ = u'rename workspace "{workspace.workspace.name}" to "{value}"'

gsm.registerUtility(
    RenameWorkspace,
    interfaces.IRenameWorkspace,
    name=RenameWorkspace.__id__)


@implementer(interfaces.IKill)
class Kill(AbstractCmd):
    __id__ = u'kill'
    __title__ = u'Kill'
    __cmd__ = u'[id="{window.window}"] kill'

gsm.registerUtility(
    Kill,
    interfaces.IKill,
    name=Kill.__id__)


@implementer(interfaces.IMoveWindowToScratchpad)
class MoveWindowToScratchpad(AbstractCmd):
    __id__ = u'move_window_to_scratchpad'
    __title__ = u'Move Window to Scratchpad'
    __cmd__ = u'[id="{window.window}"] move to scratchpad'

gsm.registerUtility(
    MoveWindowToScratchpad,
    interfaces.IMoveWindowToScratchpad,
    name=MoveWindowToScratchpad.__id__)


@implementer(interfaces.IBorder)
class Border(AbstractCmd):
    """ To change the border of the current client, you can use border normal
        to use the normal border (including window title), border pixel 1 to
        use a 1-pixel border (no window title) and border none to make the
        client borderless.

        There is also border toggle which will toggle the different border
        styles.
    """

    __id__ = u'border'
    __title__ = u'Border'
    _description = u'change the border style'
    __url__ = u'http://i3wm.org/docs/userguide.html#_changing_border_style'
    __cmd__ = u'[id="{window.window}"] border {action}'

gsm.registerUtility(
    Border,
    interfaces.IBorder,
    name=Border.__id__)


@implementer(interfaces.ISticky)
class Sticky(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_sticky_floating_windows
    """

    __id__ = u'sticky'
    __title__ = u'Sticky'
    __cmd__ = u'[id="{window.window}"] sticky {action}'

gsm.registerUtility(
    Sticky,
    interfaces.ISticky,
    name=Sticky.__id__)


@implementer(interfaces.ISplit)
class Split(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_splitting_containers
    """

    __id__ = u'split'
    __title__ = u'Split'
    __cmd__ = u'[id="{window.window}"] split {action}'

gsm.registerUtility(
    Split,
    interfaces.ISplit,
    name=Split.__id__)


@implementer(interfaces.IFullscreen)
class Fullscreen(AbstractCmd):
    """ To make the current window (!) fullscreen, use
        fullscreen enable (or fullscreen enable global for the global mode),
        to leave either fullscreen mode use fullscreen disable, and to toggle
        between these two states use fullscreen toggle (or fullscreen toggle
        global).
    """

    __id__ = u'fullscreen'
    __title__ = u'Fullscreen'
    __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    __cmd__ = u'[id="{target.window}"] fullscreen {action}'

gsm.registerUtility(
    Fullscreen,
    interfaces.IFullscreen,
    name=Fullscreen.__id__)


@implementer(interfaces.IDebuglog)
class Debuglog(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_enabling_debug_logging
    """

    __id__ = u'debuglog'
    __title__ = u'Debug Log'
    __cmd__ = u'debuglog {action}'

gsm.registerUtility(
    Debuglog,
    interfaces.IDebuglog,
    name=Debuglog.__id__)


@implementer(interfaces.IShmlog)
class Shmlog(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#shmlog
    """
    # TODO: add the possibility to specify the shared memory size

    __id__ = u'shmlog'
    __title__ = u'Shared memory Log'
    __cmd__ = u'shmlog {action}'
    _actions = [u'on', u'off', u'toggle']

gsm.registerUtility(
    Shmlog,
    interfaces.IShmlog,
    name=Shmlog.__id__)


@implementer(interfaces.IReload)
class Reload(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    __id__ = u'reload'
    __title__ = u'Reload'
    __cmd__ = u'reload'

gsm.registerUtility(
    Reload,
    interfaces.IReload,
    name=Reload.__id__)


@implementer(interfaces.IRestart)
class Restart(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    __id__ = u'restart'
    __title__ = u'Restart'
    __cmd__ = u'restart'

gsm.registerUtility(
    Restart,
    interfaces.IRestart,
    name=Restart.__id__)


@implementer(interfaces.IExit)
class Exit(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting
    """

    __id__ = u'exit'
    __title__ = u'Exit'
    __cmd__ = u'exit'

gsm.registerUtility(
    Exit,
    interfaces.IExit,
    name=Exit.__id__)


@implementer(interfaces.IGotoWorkspace)
class GotoWorkspace(AbstractCmd):

    __id__ = u'goto_workspace'
    __title__ = u'Goto Workspace'
    __cmd__ = u'workspace "{workspace.workspace.name}"'

gsm.registerUtility(
    GotoWorkspace,
    interfaces.IGotoWorkspace,
    name=GotoWorkspace.__id__)
#
#
# @implementer(interfaces.ILayout)
# class Layout(AbstractCmd):
#     """ Use layout toggle split, layout stacking, layout tabbed,
#         layout splitv or layout splith to change the current container layout
#         to splith/splitv, stacking, tabbed layout, splitv or splith,
#         respectively.
#     """
#
#     __id__ = u'exit'
#     __cmd__ = u'layout {action}'
#     __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
#     _actions = [
#         u'default', u'tabbed', u'stacking', u'splitv', u'splith',
#         u'toggle split', u'toggle all']
#
#
# @implementer(interfaces.IRenameWorkspace)
# class RenameWorkspace(AbstractCmd):
#
#     __id__ = u'rename'
#     __cmd__ = u'rename workspace "{ws.name}" to "{value}"'
