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
