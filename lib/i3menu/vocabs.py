from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtilitiesFor

from i3menu.interfaces import IWindowCommand
from i3menu.interfaces import IWorkspaceCommand


class WorkspaceObject(object):
    pass


class OutputObject(object):
    pass


class BaseVocabularyFactory(object):
    def __init__(self, context):
        self.context = context
        self._terms = [t for t in self.terms]

    @property
    def terms(self):
        return []

    def __call__(self, *args, **kwargs):
        return SimpleVocabulary(self._terms)


class WindowsVocabularyFactory(BaseVocabularyFactory):
    name = u'windows_vocabulary'

    @property
    def terms(self):
        terms = self.context.i3.get_windows()
        sortedterms = sorted(terms, key=lambda x: x.window_class)
        for t in sortedterms:
            yield SimpleTerm(t, t, t.name)


class WorkspacesVocabularyFactory(BaseVocabularyFactory):
    name = u'workspaces_vocabulary'

    @property
    def terms(self):
        terms = self.context.i3.get_workspaces()
        for term in terms:
            # this is necessary since the WorkspaceReply is a dict and
            # so it's not hashable
            ws_object = WorkspaceObject()
            ws_object.name = term.name
            ws_object.workspace = term
            yield SimpleTerm(ws_object, ws_object, ws_object.name)


class OutputsVocabularyFactory(BaseVocabularyFactory):
    name = u'outputs_vocabulary'

    @property
    def terms(self):
        terms = self.context.i3.get_active_outputs()
        for term in terms:
            # this is necessary since the WorkspaceReply is a dict and
            # so it's not hashable
            out_object = OutputObject()
            out_object.name = term.name
            out_object.output = term
            yield SimpleTerm(out_object, out_object, out_object.name)


class WindowCommandsVocabularyFactory(BaseVocabularyFactory):
    name = u'window_commands_vocabulary'

    @property
    def terms(self):
        cmds = [ut for ut in getUtilitiesFor(IWindowCommand)]
        for utname, ut in cmds:
            cname = ut.__title__
            cmd = ut
            yield SimpleTerm(cmd, cmd, cname)


class WorkspaceCommandsVocabularyFactory(BaseVocabularyFactory):
    name = u'workspace_commands_vocabulary'

    @property
    def terms(self):
        cmds = [ut for ut in getUtilitiesFor(IWorkspaceCommand)]
        for utname, ut in cmds:
            cname = ut.__title__
            cmd = ut
            yield SimpleTerm(cmd, cmd, cname)

VOCABS = [
    WindowsVocabularyFactory,
    WorkspacesVocabularyFactory,
    OutputsVocabularyFactory,
    WindowCommandsVocabularyFactory,
    WorkspaceCommandsVocabularyFactory
]


def init_vocabs(context):
    vr = getVocabularyRegistry()
    for vobject in VOCABS:
        vocab = vobject(context)
        vr = getVocabularyRegistry()
        vr.register(vobject.name, vocab)
