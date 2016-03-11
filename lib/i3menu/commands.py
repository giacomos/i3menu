import six
from zope.interface import implementer, providedBy
from zope.component import getAdapter, getGlobalSiteManager

from i3menu import _
from i3menu import logger
from i3menu import interfaces
from i3menu.menu import Menu
from i3menu.exceptions import MissingParamException

gsm = getGlobalSiteManager()


class AbstractCmd(object):
    """ Abstract command """
    __id__ = u'AbstractCmd'
    __url__ = u''
    __cmd__ = u''

    def get_defaults(self):
        defaults = {}
        for pname, param in self.params():
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

    def __call__(self, context):
        cmd_msg = None
        self.context = context
        self.data = self.get_defaults()
        self.request_params()
        cmd_msg = self.cmd(**self.data)
        if cmd_msg:
            return self.context.i3.command(cmd_msg)

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

    def params(self):
        interfaces = [i for i in providedBy(self).interfaces()]
        for i in interfaces:
            fields = [(fname, field) for fname, field in i.namesAndDescriptions()]
            fields = sorted(fields, key=lambda f: f[1].order)
            for fname, field in fields:
                yield fname, field

    def paramsdict(self):
        interfaces = [i for i in providedBy(self).interfaces()]
        res = {}
        for i in interfaces:
            fields = [(fname, field) for fname, field in i.namesAndDescriptions()]
            fields = sorted(fields, key=lambda f: f[1].order)
            for fname, field in fields:
                res[fname] = field
        return res

    def request_params(self):
        params_menu = Menu(u'params_menu', prompt=self.__title__)
        if self.validate_data():
            params_menu.add_command(label='Run!', command='run')
        missing_params = []
        present_params = []
        for fname, field in self.params():
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
            if current_value == 'N/A':
                missing_params.append((fname, label, widget))
            else:
                present_params.append((fname, label,widget))
        for p in missing_params + present_params:
            fname, label,widget = p
            entry = params_menu.add_command(
                label=label,
                command=widget)
            entry.name = fname
        res = self.context.mp.display_menu(params_menu)
        if res and res.value == 'run':
            return
        if res and res.value and interfaces.IWidget.providedBy(res.value):
            widget = res.value
            newvalue = widget()
            if newvalue:
                self.data[res.name] = newvalue
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
    __cmd__ = u'move workspace to output "{output.name}"'


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
