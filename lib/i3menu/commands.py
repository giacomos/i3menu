import six
from zope.interface import implementer, providedBy
from zope.component import getAdapter, getGlobalSiteManager
from zope.component import getUtility


from i3menu import _
from i3menu import logger
from i3menu import interfaces
from i3menu.menu import Menu
from i3menu.interfaces import II3Connector
from i3menu.exceptions import MissingParamException

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
                if isinstance(val, six.string_types):
                    current_value = val
                else:
                    current_value = val.name
            label = u'{name} = {value}'.format(
                name=fname, value=current_value)
            entry = params_menu.add_command(
                label=label,
                command=widget)
            entry.name = fname
        return self.context.mp.display_menu(params_menu)

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
