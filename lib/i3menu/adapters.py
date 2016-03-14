# -*- coding: utf-8 -*-
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.component import adapter
from zope.schema.interfaces import IVocabulary
from zope.schema.interfaces import IChoice, ITextLine, IInt

from i3menu import _
from i3menu.menu import Menu
from i3menu.interfaces import IMenu
from i3menu.interfaces import IWidget

gsm = getGlobalSiteManager()


@implementer(IMenu)
@adapter(IVocabulary)
class VocabToMenuAdapter(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, name, prompt=None):
        menu = Menu(name=name, prompt=prompt)
        for t in self.vocab:
            label = t.title and t.title or t.value
            command = t.value
            menu.add_command(label=label, command=command)
        return menu

gsm.registerAdapter(VocabToMenuAdapter)


@implementer(IWidget)
@adapter(IChoice)
class ChoiceWidget(object):

    def __init__(self, field):
        self.field = field

    def __call__(self):
        f = self.field
        f = f.bind(f.context)
        menu_adapter = IMenu(f.vocabulary)
        menu = menu_adapter(f.__name__, prompt=_(u'Select one entry'))
        res = f.context.selectinput(menu)
        if res:
            return res.value

gsm.registerAdapter(ChoiceWidget)


@implementer(IWidget)
@adapter(ITextLine)
class TextLineWidget(object):
    def __init__(self, field):
        self.field = field

    def __call__(self):
        f = self.field
        f = f.bind(f.context)
        res = f.context.textinput(prompt=f.__name__)
        if res:
            return res


gsm.registerAdapter(TextLineWidget)


@implementer(IWidget)
@adapter(IInt)
class IntWidget(object):
    def __init__(self, field):
        self.field = field

    def __call__(self):
        f = self.field
        f = f.bind(f.context)
        res = f.context.textinput(prompt=f.__name__)
        if res:
            try:
                return int(res)
            except:
                return res


gsm.registerAdapter(IntWidget)
