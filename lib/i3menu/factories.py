from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import VocabularyRegistryError

from i3menu import logger


class BaseFactory(object):
    _vname = u''

    def terms(self):
        vr = getVocabularyRegistry()
        try:
            vocab = vr.get({}, self._vname)
        except VocabularyRegistryError:
            logger.error('Vocabulary not found: ' + self._vname)
            return
        return [i for i in vocab]


class FocusedWindowFactory(BaseFactory):
    _vname = u'windows_vocabulary'

    def __call__(self):
        for term in self.terms():
            win = term.value
            if win.focused:
                return win


class FocusedWorkspaceFactory(BaseFactory):
    _vname = u'workspaces_vocabulary'

    def __call__(self):
        for term in self.terms():
            ws = term.value
            if ws.workspace.focused:
                return ws
