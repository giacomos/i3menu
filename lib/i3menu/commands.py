from zope.interface import alsoProvides
from zope.interface import provider
from zope.interface.verify import verifyObject
from zope.component import getAdapter, getGlobalSiteManager
from zope.component import getUtility
from zope.schema import getValidationErrors
from zope.schema.interfaces import RequiredMissing

from i3menu import _
from i3menu import logger
from i3menu import interfaces
from i3menu.menu import Menu
from i3menu.interfaces import II3Connector

gsm = getGlobalSiteManager()


class Form(object):
    def __init__(self, fields, data=None):
        fields = [(fname, f.bind(self)) for fname, f in fields]
        self._fields = fields
        tmpdata = {k: None for k, v in fields}
        tmpdata.update(data)
        self._data = tmpdata

    @property
    def _fieldsdict(self):
        return {f[0]: f[1] for f in self._fields}

    def __getattr__(self, attr):
        if attr == '_fieldsdict':
            return self._fieldsdict
        elif attr == '_fields':
            return self._fields
        elif attr in self._data:
            return self._data[attr]

    def add_field(self, fname, field):
        self._fields.append((fname, field))
        self._data[fname] = self._data.get(fname) or None

    def missing_fields(self):
        return [
            (fname, field)
            for fname, field in self._fields if not getattr(self, fname)]

    def present_fields(self):
        return [
            (fname, field)
            for fname, field in self._fields if getattr(self, fname)]

    def fields(self):
        missing_fields = self.missing_fields()
        present_fields = self.present_fields()
        fields = [(fname, f)
                  for fname, f in missing_fields + present_fields if f.visible]
        return fields


class AbstractCmd(object):
    """ Abstract command """
    __component_name__ = u'AbstractCmd'
    __title__ = _(u'Abstract Command')
    __url__ = u''
    __cmd__ = u''
    schema = None

    def __init__(self, context):
        self.context = context
        data = {}
        fields = [p for p in self._get_fields_from_interfaces()]
        data.update(self.get_defaults(fields))
        self.form = Form(fields, data)
        self.form.action
        if self.schema:
            alsoProvides(self.form, self.schema)
            assert verifyObject(self.schema, self.form)

    def _get_fields_from_interfaces(self):
        fields = []
        if self.schema:
            fields = [(fname, field)
                      for fname, field in self.schema.namesAndDescriptions()]
        fields = sorted(fields, key=lambda f: f[1].order)
        for fname, field in fields:
            yield fname, field

    def get_defaults(self, fields):
        defaults = {fname: field.default
                    for fname, field in fields if field.default}
        return defaults

    def validate(self):
        # allfields = self.fieldsdict()
        # # first we need to bind all fields to the data object
        # for fname in allfields:
        #     field = allfields[fname]
        #     field.bind(self.form)
        errors = []
        errors = getValidationErrors(self.schema, self.form)
        errorsdict = {}
        for field, error in errors:
            errorsdict[field] = error
        return errorsdict

    def __call__(self):
        cmd_msg = None
        self.request_fields()
        cmd_msg = self.cmd()
        if cmd_msg:
            conn = getUtility(II3Connector)
            logger.debug('Run command: {cmd}'.format(cmd=cmd_msg))
            return conn.command(cmd_msg)

    def cmd(self):
        errors = self.validate()
        if not errors:
            return self.__cmd__.format(**self.form._data)

    def fields_summary_menu(self):
        fields_menu = Menu(u'fields_menu', prompt=self.__title__)
        errors = self.validate()
        if not errors:
            fields_menu.add_command(label='Run!', command='run')
        fields = self.form.fields()
        for fname, field in fields:
            field = field.bind(self.context)
            widget = getAdapter(field, interfaces.IWidget)
            current_value = 'N/A'
            error_msg = ''
            if fname in errors:
                error = errors[fname]
                if not isinstance(error, RequiredMissing):
                    error_msg = ' [Error: {msg}]'.format(msg=repr(error))
            val = getattr(self.form, fname)
            if hasattr(val, 'name'):
                current_value = val
                current_value = val.name
            elif val:
                current_value = val
            name = field.title or fname
            label = u'{name} = {value}{error_msg}'.format(
                name=name, value=current_value, error_msg=error_msg)
            entry = fields_menu.add_command(
                label=label,
                command=widget,
                error=errors.get(fname))
            entry.name = fname
        return self.context.selectinput(fields_menu)

    def request_fields(self):
        res = self.fields_summary_menu()
        if not res or res.value == 'run':
            return
        elif interfaces.IWidget.providedBy(res.value):
            widget = res.value
            newvalue = widget()
            self.form._data[res.name] = newvalue
        self.request_fields()


###############################
#
# WORKSPACE ACTIONS
#
###############################


@provider(interfaces.IWorkspaceCommand)
class MoveWorkspaceToOutput(AbstractCmd):
    """
    http://i3wm.org/docs/userguide.html#_moving_workspaces_to_a_different_screen
    """
    # XXX: it seems that it's not possible to specify a workspace other
    # than the current one. This needs to be investigated further
    __component_name__ = u'move_workspace_to_output'
    __title__ = u'Move Workspace To Output'
    __cmd__ = u'move workspace to output "{output.output.name}"'
    schema = interfaces.IMoveWorkspaceToOutput

gsm.registerUtility(MoveWorkspaceToOutput)


@provider(interfaces.IWorkspaceCommand)
class RenameWorkspace(AbstractCmd):
    __component_name__ = u'rename'
    __title__ = u'Rename workspace'
    __cmd__ = u'rename workspace "{workspace.workspace.name}" to "{value}"'
    schema = interfaces.IRenameWorkspace

gsm.registerUtility(RenameWorkspace)


@provider(interfaces.IWorkspaceCommand)
class Layout(AbstractCmd):
    """ Use layout toggle split, layout stacking, layout tabbed,
        layout splitv or layout splith to change the current container layout
        to splith/splitv, stacking, tabbed layout, splitv or splith,
        respectively.
    """

    __component_name__ = u'layout'
    __title__ = u'Layout'
    __cmd__ = u'layout {action}'
    __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    schema = interfaces.ILayout

gsm.registerUtility(Layout)


###############################
#
# window actions
#
###############################


@provider(interfaces.IWindowCommand)
class Resize(AbstractCmd):
    __component_name__ = u'resize'
    __title__ = _(u'Resize')
    __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    __cmd__ = u'resize {action} {direction}'
    schema = interfaces.IResize

    def cmd(self, *args, **kwargs):
        cmd = ''
        errors = self.validate()
        if errors:
            return cmd
        data = self.data.__dict__.copy()
        action = data.get('action')
        if action in ['grow', 'shrink']:
            cmd = '[id="{window.window}"] resize {action} {direction}'.format(
                window=data.get('window'), action=action,
                direction=data.get('direction'))
            if 'pixels' in data:
                cmd += ' {pixels} px'.format(pixels=data['pixels'])
            elif 'ppt' in data:
                cmd += ' {ppt}'.format(ppt=data['ppt'])
        elif action == 'set':
            cmd = '[id="{window.window}"] resize {action} {width} px {height} px'.format(  # noqa
                window=data.get('window'), action=action,
                width=data['width'], height=data['height'])
        return cmd

gsm.registerUtility(Resize)


@provider(interfaces.IWindowCommand)
class Floating(AbstractCmd):
    __component_name__ = u'floating'
    __title__ = _(u'Floating')
    __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    __cmd__ = u'[id="{window.window}"] floating {action}'
    schema = interfaces.IFloating

gsm.registerUtility(Floating)


@provider(interfaces.IWindowCommand)
class MoveWindowToWorkspace(AbstractCmd):
    __component_name__ = u'move_window_to_workspace'
    __title__ = _(u'Move Window To Workspace')
    __cmd__ = u'[id="{window.window}"] move window to workspace '\
        '"{workspace.workspace.name}"'
    schema = interfaces.IMoveWindowToWorkspace

gsm.registerUtility(MoveWindowToWorkspace)


@provider(interfaces.IWindowCommand)
class Kill(AbstractCmd):
    __component_name__ = u'kill'
    __title__ = u'Kill'
    __cmd__ = u'[id="{window.window}"] kill'
    schema = interfaces.IKill

gsm.registerUtility(Kill)


@provider(interfaces.IWindowCommand)
class MoveWindowToScratchpad(AbstractCmd):
    __component_name__ = u'move_window_to_scratchpad'
    __title__ = u'Move Window to Scratchpad'
    __cmd__ = u'[id="{window.window}"] move to scratchpad'
    schema = interfaces.IMoveWindowToScratchpad

gsm.registerUtility(MoveWindowToScratchpad)


@provider(interfaces.IWindowCommand)
class Border(AbstractCmd):
    """ To change the border of the current client, you can use border normal
        to use the normal border (including window title), border pixel 1 to
        use a 1-pixel border (no window title) and border none to make the
        client borderless.

        There is also border toggle which will toggle the different border
        styles.
    """

    __component_name__ = u'border'
    __title__ = u'Border'
    _description = u'change the border style'
    __url__ = u'http://i3wm.org/docs/userguide.html#_changing_border_style'
    __cmd__ = u'[id="{window.window}"] border {action}'
    schema = interfaces.IBorder

gsm.registerUtility(Border)


@provider(interfaces.IWindowCommand)
class Sticky(AbstractCmd):
    __component_name__ = u'sticky'
    __title__ = u'Sticky'
    __cmd__ = u'[id="{window.window}"] sticky {action}'
    __url__ = u'http://i3wm.org/docs/userguide.html#_sticky_floating_windows'
    schema = interfaces.ISticky

gsm.registerUtility(Sticky)


@provider(interfaces.ISplit)
class Split(AbstractCmd):
    __component_name__ = u'split'
    __title__ = u'Split'
    __url__ = u'http://i3wm.org/docs/userguide.html#_splitting_containers'
    __cmd__ = u'[id="{window.window}"] split {action}'
    schema = interfaces.ISplit

gsm.registerUtility(Split)


@provider(interfaces.IWindowCommand)
class Fullscreen(AbstractCmd):
    __component_name__ = u'fullscreen'
    __title__ = u'Fullscreen'
    __url__ = u'http://i3wm.org/docs/userguide.html#_manipulating_layout'
    __cmd__ = u'[id="{target.window}"] fullscreen {action}'
    schema = interfaces.IFullscreen

gsm.registerUtility(Fullscreen)


###############################
#
# GLOBAL ACTIONS
#
###############################


@provider(interfaces.IGlobalCommand)
class Debuglog(AbstractCmd):
    __component_name__ = u'debuglog'
    __title__ = u'Debug Log'
    __url__ = u'http://i3wm.org/docs/userguide.html#_enabling_debug_logging'
    __cmd__ = u'debuglog {action}'
    schema = interfaces.IDebuglog

gsm.registerUtility(Debuglog)


@provider(interfaces.IGlobalCommand)
class Shmlog(AbstractCmd):
    __component_name__ = u'shmlog'
    __title__ = u'Shared memory Log'
    __url__ = u'http://i3wm.org/docs/userguide.html#shmlog'
    __cmd__ = u'shmlog {action}'
    schema = interfaces.IShmlog

    def cmd(self, *args, **kwargs):
        errors = self.validate()
        if errors:
            return ''
        elif self.data.size:
            return u'shmlog {size}'
        elif self.data.action:
            return u'shmlog {action}'

gsm.registerUtility(Shmlog)


@provider(interfaces.IGlobalCommand)
class Reload(AbstractCmd):
    __component_name__ = u'reload'
    __title__ = u'Reload'
    __url__ = u'http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting'  # noqa
    __cmd__ = u'reload'
    schema = interfaces.IReload

gsm.registerUtility(Reload)


@provider(interfaces.IGlobalCommand)
class Restart(AbstractCmd):
    __component_name__ = u'restart'
    __title__ = u'Restart'
    __url__ = u'http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting'  # noqa
    __cmd__ = u'restart'
    schema = interfaces.IRestart

gsm.registerUtility(Restart)


@provider(interfaces.IGlobalCommand)
class Exit(AbstractCmd):
    __component_name__ = u'exit'
    __title__ = u'Exit'
    __url__ = u'http://i3wm.org/docs/userguide.html#_reloading_restarting_exiting'  # noqa
    __cmd__ = u'exit'
    schema = interfaces.IExit

gsm.registerUtility(Exit)


###############################
#
# GOTO ACTIONS
#
###############################


@provider(interfaces.IGotoCommand)
class GotoWindow(AbstractCmd):
    __component_name__ = u'goto_window'
    __title__ = u'Goto Window'
    __cmd__ = u'[id="{window.window}"] focus'
    schema = interfaces.IGotoWindow

gsm.registerUtility(GotoWindow)


@provider(interfaces.IGotoCommand)
class GotoWorkspace(AbstractCmd):
    __component_name__ = u'goto_workspace'
    __title__ = u'Goto Workspace'
    __cmd__ = u'workspace "{workspace.workspace.name}"'
    schema = interfaces.IGotoWorkspace

gsm.registerUtility(GotoWorkspace)
