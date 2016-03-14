from zope.interface import Interface
from i3menu.fields import Choice, Int, TextLine
from i3menu.factories import FocusedWindowFactory, FocusedWorkspaceFactory


class II3Connector(Interface):
    """"""


class IContextManager(Interface):
    """"""


class IWidget(Interface):
    """"""


class IMenu(Interface):
    """"""


class IMenuProvider(Interface):
    """"""


class IWindowObject(Interface):
    """ Window Object """


class IFocusedWindowObject(IWindowObject):
    """ Focused Window Object """


class ICommand(Interface):
    """"""


class IWindowCommand(ICommand):
    """"""


class IWorkspaceCommand(ICommand):
    """"""


class IGlobalCommand(ICommand):
    """"""


class IGotoCommand(ICommand):
    """"""


class IScratchpadCommand(ICommand):
    """"""


class IBarCommand(ICommand):
    """"""


###############################
#
# WORKSPACE ACTIONS
#
###############################


class IMoveWorkspaceToOutput(Interface):
    output = Choice(
        title=u"Output",
        required=True,
        vocabulary="outputs_vocabulary",
    )

    # workspace = Choice(
    #     title=u"Workspace",
    #     required=False,
    #     vocabulary="workspaces_vocabulary",
    # )


class IRenameWorkspace(Interface):

    workspace = Choice(
        title=u"Workspace",
        required=False,
        vocabulary="workspaces_vocabulary",
        defaultFactory=FocusedWorkspaceFactory()
    )

    value = TextLine(
        title=u"New name",
        required=True,
    )


class ILayout(Interface):

    action = Choice(
        title=u"Action",
        required=False,
        default='toggle all',
        values=[
            u'default', u'tabbed', u'stacking', u'splitv', u'splith',
            u'toggle split', u'toggle all']
    )


###############################
#
# window actions
#
###############################


class IResize(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )
    action = Choice(
        title=u"Action",
        required=True,
        values=['grow', 'shrink', 'set']
    )
    direction = Choice(
        title=u"Direction",
        required=False,
        values=['up', 'down', 'left', 'right'],
        visible_condition=lambda ctx: ctx.action in ['grow', 'shrink'],
        required_condition=lambda ctx: ctx.action in ['grow', 'shrink']
    )
    pixels = Int(
        title=u"Pixels",
        required=False,
        min=0,
        visible_condition=lambda ctx: ctx.action in ['grow', 'shrink'] and not ctx.ppt,  # noqa
    )
    ppt = Int(
        title=u"Ppt",
        required=False,
        min=0,
        max=100,
        visible_condition=lambda ctx: ctx.action in ['grow', 'shrink'] and not ctx.pixels,  # noqa
    )
    width = TextLine(
        title=u"Width",
        required=False,
        visible_condition=lambda ctx: ctx.action in ['set'],
        required_condition=lambda ctx: ctx.action in ['set']
    )
    height = TextLine(
        title=u"Height",
        required=False,
        visible_condition=lambda ctx: ctx.action in ['set'],
        required_condition=lambda ctx: ctx.action in ['set']
    )


class IFloating(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=True,
        default='toggle',
        values=['enable', 'disable', 'toggle']
    )


class IMoveWindowToWorkspace(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    workspace = Choice(
        title=u"Workspace",
        required=True,
        vocabulary="workspaces_vocabulary",
    )


class IKill(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )


class IMoveWindowToScratchpad(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )


class IBorder(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=True,
        default='toggle',
        values=[u'none', u'normal', u'pixel 1', u'pixel 3', u'toggle']
    )


class ISticky(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=True,
        default='toggle',
        values=[u'enable', u'disable', u'toggle']
    )


class ISplit(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=True,
        values=[u'vertical', u'horizontal']
    )


class IFullscreen(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=True,
        default='toggle',
        values=[u'enable', u'disable', u'toggle']
    )


###############################
#
# GLOBAL ACTIONS
#
###############################


class IDebuglog(Interface):
    action = Choice(
        title=u"Action",
        required=True,
        default='toggle',
        values=[u'on', u'off', u'toggle']
    )


class IShmlog(Interface):
    action = Choice(
        title=u"Action",
        required=False,
        # default='toggle',
        values=[u'on', u'off', u'toggle'],
        visible_condition=lambda ctx: not ctx.size,
        required_condition=lambda ctx: not ctx.size
    )
    size = Int(
        title=u"Size (bytes)",
        required=False,
        min=0,
        visible_condition=lambda ctx: not ctx.action,
        required_condition=lambda ctx: not ctx.action
    )


class IReload(Interface):
    """"""


class IRestart(Interface):
    """"""


class IExit(Interface):
    """"""


###############################
#
# GOTO ACTIONS
#
###############################


class IGotoWindow(Interface):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
    )


class IGotoWorkspace(Interface):
    workspace = Choice(
        title=u"Workspace",
        required=True,
        vocabulary="workspaces_vocabulary",
    )
