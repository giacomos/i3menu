from collections import OrderedDict
from zope.interface import implementer
from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import SimpleTerm, TreeVocabulary, SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtilitiesFor, getUtility

from i3menu.interfaces import IWindowCommand
from i3menu.interfaces import IWorkspaceCommand
from i3menu.interfaces import IMoveCommand
from i3menu.interfaces import IGlobalCommand
from i3menu.interfaces import IFocusCommand
from i3menu.interfaces import IScratchpadCommand
from i3menu.interfaces import IBarCommand
from i3menu.interfaces import II3Connector


class WorkspaceObject(object):
    pass


class OutputObject(object):
    pass


@implementer(IVocabularyFactory)
class BaseVocabularyFactory(object):
    def __init__(self):
        self._terms = [t for t in self.terms]

    @property
    def terms(self):
        return []

    def __call__(self, *args, **kwargs):
        return SimpleVocabulary([SimpleTerm(*t) for t in self._terms])


class WindowsVocabularyFactory(BaseVocabularyFactory):
    name = u'windows_vocabulary'

    @property
    def terms(self):
        conn = getUtility(II3Connector)
        terms = conn.get_windows()
        sortedterms = sorted(terms, key=lambda x: x.window_class)
        for t in sortedterms:
            yield (t, t, t.name)


class ScratchpadWindowsVocabularyFactory(BaseVocabularyFactory):
    name = u'scratchpad_windows_vocabulary'

    @property
    def terms(self):
        conn = getUtility(II3Connector)
        terms = conn.get_scratchpad_windows()
        sortedterms = sorted(terms, key=lambda x: x.window_class)
        for t in sortedterms:
            yield (t, t, t.name)


class MarksVocabularyFactory(BaseVocabularyFactory):
    name = u'marks_vocabulary'

    @property
    def terms(self):
        conn = getUtility(II3Connector)
        terms = conn.get_marks()
        for t in terms:
            yield (t, t, t)


class WorkspacesVocabularyFactory(BaseVocabularyFactory):
    name = u'workspaces_vocabulary'

    @property
    def terms(self):
        conn = getUtility(II3Connector)
        terms = conn.get_workspaces()
        for term in terms:
            # this is necessary since the WorkspaceReply is a dict and
            # so it's not hashable
            ws_object = WorkspaceObject()
            ws_object.name = term.name
            ws_object.workspace = term
            yield (ws_object, ws_object, ws_object.name)


class OutputsVocabularyFactory(BaseVocabularyFactory):
    name = u'outputs_vocabulary'

    @property
    def terms(self):
        conn = getUtility(II3Connector)
        terms = conn.get_active_outputs()
        for term in terms:
            # this is necessary since the WorkspaceReply is a dict and
            # so it's not hashable
            out_object = OutputObject()
            out_object.name = term.name
            out_object.output = term
            yield (out_object, out_object, out_object.name)


class BaseCommandsVocabularyFactory(BaseVocabularyFactory):

    interface = None

    @property
    def terms(self):
        cmds = [ut for ut in getUtilitiesFor(self.interface)]
        cmds = sorted(cmds, key=lambda i: i[1].priority, reverse=True)
        for utname, ut in cmds:
            # value, token, title
            yield (ut, utname, ut.__title__)


class WindowCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'window_actions'
    title = u'Windows'

    interface = IWindowCommand


class WorkspaceCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'workspace_actions'
    title = u'Workspaces'

    interface = IWorkspaceCommand


class MoveCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'move_actions'
    title = u'Move...'

    interface = IMoveCommand


class GlobalCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'global_actions'
    title = u'i3'

    interface = IGlobalCommand


class FocusCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'focus_actions'
    title = u'Focus...'

    interface = IFocusCommand


class ScratchpadCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'scratchpad_actions'
    title = u'Scratchpad'

    interface = IScratchpadCommand


class BarCommandsVocabularyFactory(BaseCommandsVocabularyFactory):
    name = u'bar_actions'
    title = u'Bars'

    interface = IBarCommand


class RootMenu(object):
    subvocabs = [
        FocusCommandsVocabularyFactory,
        MoveCommandsVocabularyFactory,
        WindowCommandsVocabularyFactory,
        WorkspaceCommandsVocabularyFactory,
        ScratchpadCommandsVocabularyFactory,
        BarCommandsVocabularyFactory,
        GlobalCommandsVocabularyFactory
    ]

    def __call__(self):
        # terms = []
        # for vf_klass in self.subvocabs:
        #     term = SimpleTerm(vf_klass, vf_klass.name, vf_klass.title)
        #     terms.append(term)
        # return SimpleVocabulary(terms)
        menus = OrderedDict()
        for submenucls in self.subvocabs:
            submenu = submenucls()
            # (value, token, title)
            entry = (submenu.name, submenu, submenu.title)
            values = OrderedDict()
            for cmd in submenu.terms:
                values[cmd] = {}
            menus[entry] = values
        tv = TreeVocabulary.fromDict(menus)
        return tv


# menu = RootMenu()
# menu()

VOCABS = [
    WindowsVocabularyFactory,
    WorkspacesVocabularyFactory,
    OutputsVocabularyFactory,
    WindowCommandsVocabularyFactory,
    WorkspaceCommandsVocabularyFactory,
    MoveCommandsVocabularyFactory,
    GlobalCommandsVocabularyFactory,
    FocusCommandsVocabularyFactory,
    ScratchpadCommandsVocabularyFactory,
    BarCommandsVocabularyFactory,
    ScratchpadWindowsVocabularyFactory,
    MarksVocabularyFactory
]


def init_vocabs():
    vr = getVocabularyRegistry()
    for vobject in VOCABS:
        vocab = vobject()
        vr.register(vobject.name, vocab)
