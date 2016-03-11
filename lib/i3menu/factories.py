from zope.interface import implementer
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import VocabularyRegistryError

from i3menu import logger


@implementer(IContextAwareDefaultFactory)
class FocusedWindowFactory(object):
    def __call__(self, context, vname='windows_vocabulary'):
        vr = getVocabularyRegistry()
        try:
            vocab = vr.get(context, vname)
        except VocabularyRegistryError:
            logger.error('Vocabulary not found: ' + vname)
            return
        terms = [i for i in vocab]
        for term in terms:
            win = term.value
            if win.focused:
                return win


@implementer(IContextAwareDefaultFactory)
class FocusedWorkspaceFactory(object):
    def __call__(self, context, vname='workspaces_vocabulary'):
        vr = getVocabularyRegistry()
        try:
            vocab = vr.get(context, vname)
        except VocabularyRegistryError:
            logger.error('Vocabulary not found: ' + vname)
            return
        terms = [i for i in vocab]
        for term in terms:
            ws = term.value
            if ws.workspace.focused:
                return ws
