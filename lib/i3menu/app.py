# -*- coding: utf-8 -*-
import logging

from i3menu import _, __name__, logger
from i3menu.config import DEFAULTS
from i3menu.interfaces import IMenuProvider
from i3menu.interfaces import IContextManager
from i3menu.interfaces import ICommand
from i3menu.interfaces import IWidget
from i3menu.exceptions import MenuProviderNotFound, NoInputError
from i3menu.vocabs import RootMenu
from i3menu.fields import Choice
from zope.component import getAdapter

from zope.component import getUtility, getUtilitiesFor, ComponentLookupError
from i3menu.vocabs import init_vocabs


class Application(object):
    __name__ = __name__

    def __init__(self, args=None):
        self.context = getUtility(IContextManager)
        self.context.config = self.parse_args(args)
        self.context.mp = self.get_menu_provider()
        init_vocabs()
        rmv = RootMenu()
        self.tree = rmv()
        self.tree.title = _(u'Root')

    def parse_args(self, params=None):
        config = DEFAULTS
        if not params:
            return config
        if params.debug:
            config['debug'] = True
        if params.menu_provider:
            config['menu_provider'] = params.menu_provider
        if params.menu:
            config['root'] = params.menu
        return config

    def apply_config(self):
        if self.context.config.get('debug'):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)
        if not self.context.mp:
            logger.info(u'No menu provider found. Testing?')
        if self.context.config.get('root'):
            m = self.context.config['root']
            try:
                term = self.tree.getTermByToken(m)
                self.tree = term.value()
                self.tree.title = term.title
            except LookupError:
                msg = u'Menu "{name}" not found. Using root menu instead'\
                    .format(name=m)
                logger.warning(msg)
                pass
            else:
                logger.info(u'Initial root: {root}'.format(root=self.tree))

    def mainloop(self, tree, prompt=None):
        prompt = prompt or tree.title
        field = Choice(
            title=prompt,
            vocabulary=tree
        )
        field = field.bind(self.context)
        widget = getAdapter(field, IWidget)
        choice = widget()
        if not choice:
            return
        if ICommand.implementedBy(choice.value):
            return choice.value
        vf = choice.value()
        newtree = vf
        newtree.parent = tree
        return self.mainloop(newtree, prompt=choice.title)

    def run(self):
        self.apply_config()
        try:
            cmd_klass = self.mainloop(self.tree)
            cmd = cmd_klass(self.context)
            res = cmd()
        except NoInputError:
            logger.info(u'Ok see you soon! Bye! :)')
            return 0
        if not res or not len(res):
            logger.info(u'The command made no changes on i3')
            return 0
        elif res[0].get('success'):
            logger.info(u'All done. Bye! :)')
            return 0
        else:
            return res[0].get('error')

    def get_menu_provider(self):
        mps = getUtilitiesFor(IMenuProvider)
        mps = [ut for name, ut in mps]
        mps = sorted(mps, key=lambda x: x.priority, reverse=True)
        required_provider = self.context.config.get('menu_provider')
        if required_provider:
            try:
                ut = getUtility(IMenuProvider, name=required_provider)
                return ut
            except ComponentLookupError:
                logger.warning(
                    'No menu provider found for name: %s' % required_provider)
                raise MenuProviderNotFound
        return mps[0]


if __name__ == '__main__':
    app = Application()
    app.run()
