from zope.interface import implementer
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.vocabulary import getVocabularyRegistry

vr = getVocabularyRegistry()


@implementer(IContextAwareDefaultFactory)
class FocusedWindowFactory(object):
    def __call__(self, context):
        vocab = vr.get(context, 'windows_vocabulary')
        terms = [i for i in vocab]
        for term in terms:
            win = term.value
            if win.focused:
                return win

focused_window = FocusedWindowFactory()


@implementer(IContextAwareDefaultFactory)
class FocusedWorkspaceFactory(object):
    def __call__(self, context):
        vocab = vr.get(context, 'workspaces_vocabulary')
        terms = [i for i in vocab]
        for term in terms:
            ws = term.value
            if ws.workspace.focused:
                return ws

focused_workspace = FocusedWorkspaceFactory()
