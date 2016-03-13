from zope.interface import Interface
from zope.schema import Choice, TextLine
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


class IFloating(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=False,
        default='toggle',
        values=['enable', 'disable', 'toggle']
    )


class IMoveWindowToWorkspace(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    workspace = Choice(
        title=u"Workspace",
        required=False,
        vocabulary="workspaces_vocabulary",
    )


class IMoveWorkspaceToOutput(IWorkspaceCommand):
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


class IRenameWorkspace(IWorkspaceCommand):

    workspace = Choice(
        title=u"Workspace",
        required=False,
        vocabulary="workspaces_vocabulary",
        defaultFactory=FocusedWorkspaceFactory()
    )

    value = TextLine(
        title=u"Title",
        required=True,
    )


class IKill(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )


class IMoveWindowToScratchpad(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )


class IBorder(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=False,
        default='toggle',
        values=[u'none', u'normal', u'pixel 1', u'pixel 3', u'toggle']
    )


class ISticky(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=False,
        default='toggle',
        values=[u'enable', u'disable', u'toggle']
    )


class ISplit(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=False,
        values=[u'vertical', u'horizontal']
    )


class IFullscreen(IWindowCommand):
    window = Choice(
        title=u"Window",
        required=True,
        vocabulary="windows_vocabulary",
        defaultFactory=FocusedWindowFactory()
    )

    action = Choice(
        title=u"Action",
        required=False,
        default='toggle',
        values=[u'enable', u'disable', u'toggle']
    )


class IDebuglog(IGlobalCommand):
    action = Choice(
        title=u"Action",
        required=False,
        default='toggle',
        values=[u'on', u'off', u'toggle']
    )


class IShmlog(IGlobalCommand):
    action = Choice(
        title=u"Action",
        required=False,
        default='toggle',
        values=[u'on', u'off', u'toggle']
    )


class IReload(IGlobalCommand):
    """"""


class IRestart(IGlobalCommand):
    """"""


class IExit(IGlobalCommand):
    """"""


class IGotoWorkspace(IGotoCommand):
    workspace = Choice(
        title=u"Workspace",
        required=False,
        vocabulary="workspaces_vocabulary",
    )
