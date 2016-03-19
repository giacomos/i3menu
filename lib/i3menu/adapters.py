# -*- coding: utf-8 -*-
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.component import adapter
from zope.schema.interfaces import IChoice, ITextLine, IInt

from i3menu import _
from i3menu.interfaces import IWidget

gsm = getGlobalSiteManager()


@implementer(IWidget)
@adapter(IChoice)
class ChoiceWidget(object):

    def __init__(self, field):
        self.field = field

    def __call__(self):
        f = self.field
        f = f.bind(f.context)
        return f.context.selectinput(
            f.vocabulary, prompt=f.title)

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
