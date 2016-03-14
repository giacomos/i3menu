# -*- coding: utf-8 -*-
import sys
import logging
from zope.schema.vocabulary import getVocabularyRegistry

from i3menu import _, __name__, logger
from i3menu.config import DEFAULTS
from i3menu.menu import menu_root
from i3menu.menu import Menu, MenuEntry
from i3menu.interfaces import IMenuProvider
from i3menu.interfaces import IContextManager
from i3menu.interfaces import IMenu
from i3menu.exceptions import MenuProviderNotFound

from zope.component import getUtility, getUtilitiesFor, ComponentLookupError
from i3menu.vocabs import init_vocabs


class Application(object):
    __name__ = __name__

    def __init__(self, args=None):
        self.context = getUtility(IContextManager)
        self.context.config = self.parse_args(args)
        self.context.mp = self.get_menu_provider()
        init_vocabs()

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
        self.tree = self.build_menu_tree()
        if self.context.config.get('root'):
            self.tree = menu_root(self.tree, self.context.config['root'])
            self.tree.root = True
            logger.info(u'Initial root: {root}'.format(root=self.tree))

    def build_menu_tree(self):
        vr = getVocabularyRegistry()
        window_commands_vocab = vr.get(
            self.context, 'window_commands_vocabulary')
        window_commands_vocab._name = u'window_actions'
        menu_adapter = IMenu(window_commands_vocab)
        window_menu = menu_adapter(
            name=u'window_actions', prompt=_(u'Windows Actions'))

        workspace_commands_vocab = vr.get(
            self.context, 'workspace_commands_vocabulary')
        menu_adapter = IMenu(workspace_commands_vocab)
        workspace_menu = menu_adapter(
            name=u'workspace_actions', prompt=_(u'Workspace Actions'))

        goto_commands_vocab = vr.get(
            self.context, 'goto_commands_vocabulary')
        menu_adapter = IMenu(goto_commands_vocab)
        goto_menu = menu_adapter(
            u'goto_actions', prompt=_(u'Goto actions'))
        bar_commands_vocab = vr.get(
            self.context, 'bar_commands_vocabulary')
        menu_adapter = IMenu(bar_commands_vocab)
        bar_menu = menu_adapter(
            u'bar_actions', prompt=_(u'Bar actions'))
        global_commands_vocab = vr.get(
            self.context, 'global_commands_vocabulary')
        menu_adapter = IMenu(global_commands_vocab)
        global_menu = menu_adapter(
            u'global_actions', prompt=_(u'Global actions'))
        scratchpad_commands_vocab = vr.get(
            self.context, 'scratchpad_commands_vocabulary')
        menu_adapter = IMenu(scratchpad_commands_vocab)
        scratchpad_menu = menu_adapter(
            u'scratchpad_actions', prompt=_(u'Scratchpad actions'))

        root_menu = Menu('root', prompt=_(u'Root'), root=True)
        root_menu.add_cascade(
            label=goto_menu.prompt, menu=goto_menu)
        root_menu.add_cascade(
            label=window_menu.prompt, menu=window_menu)
        root_menu.add_cascade(
            label=workspace_menu.prompt, menu=workspace_menu)
        root_menu.add_cascade(
            label=bar_menu.prompt, menu=bar_menu)
        root_menu.add_cascade(
            label=scratchpad_menu.prompt, menu=scratchpad_menu)
        root_menu.add_cascade(
            label=global_menu.prompt, menu=global_menu)
        return root_menu

    def run(self):
        self.apply_config()
        parent_menu = self.tree
        res = self.context.selectinput(parent_menu)

        while(isinstance(res, MenuEntry) and isinstance(res.value, Menu)):
            menu = res.value
            menu.parent = parent_menu
            res = self.context.selectinput(menu)
        if not res or not res.value:
            logger.info(u'Done! Cheers, bye! :)')
            sys.exit()
        cmd_klass = res.value
        cmd = cmd_klass(self.context)
        res = cmd()
        if not res or not len(res):
            logger.info(u'The command made no changes on i3')
            return
        elif res[0].get('success'):
            logger.info(u'Done! Cheers, bye! :)')
            return
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
