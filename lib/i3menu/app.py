# -*- coding: utf-8 -*-
import sys
import logging
import six

from i3menu.connector import I3Connector
from i3menu.utils import which
from i3menu.config import DEFAULTS
from i3menu import _
from i3menu import __name__
from i3menu import logger
from i3menu import cmds
from i3menu.menu import menu_root
from i3menu.menu import Menu
from i3menu.menu import display_menu
from i3menu.menu import mainloop


def menu_tree():

    window_entries_menu = Menu(
        u'window_actions', prompt=_(u'Window Actions'))
    window_entries_menu.add_command(
        label=_(u'Move window to workspace'),
        command=cmds.MoveWindowToWorkspaceCmd)
    window_entries_menu.add_command(
        label=_(u'Border style'), command=cmds.BorderCmd)
    window_entries_menu.add_command(
        label=_(u'Split'), command=cmds.SplitCmd)
    window_entries_menu.add_command(
        label=_(u'Floating (toggle)'), command=cmds.FloatingCmd)
    window_entries_menu.add_command(
        label=_(u'Fullscreen (toggle)'), command=cmds.FullscreenCmd)
    window_entries_menu.add_command(
        label=_(u'Sticky'), command=cmds.StickyCmd)
    window_entries_menu.add_command(
        label=_(u'Move to Scratchpad'),
        command=cmds.MoveWindowToScratchpadCmd)
    window_entries_menu.add_command(
        label=_(u'Kill'), command=cmds.KillCmd)

    workspace_entries_menu = Menu(
        u'workspace_actions', prompt=_(u'Workspace Actions'))
    workspace_entries_menu.add_command(
        label=_(u'Rename'),
        command=cmds.RenameWorkspaceCmd)
    workspace_entries_menu.add_command(
        label=_(u'Layout'),
        command=cmds.LayoutCmd)
    workspace_entries_menu.add_command(
        label=_(u'Move workspace to output'),
        command=cmds.MoveWorkspaceToOutputCmd)

    global_entries_menu = Menu(
        u'global_actions', prompt=_(u'Global actions'))
    global_entries_menu.add_command(
        label=_(u'Debug log'), command=cmds.DebuglogCmd)
    global_entries_menu.add_command(
        label=_(u'Shared memory log'), command=cmds.ShmlogCmd)
    global_entries_menu.add_command(
        label=_(u'Restart i3'), command=cmds.RestartCmd)
    global_entries_menu.add_command(
        label=_(u'Reload i3'), command=cmds.ReloadCmd)
    global_entries_menu.add_command(
        label=_(u'Exit i3'), command=cmds.ExitCmd)

    goto_entries_menu = Menu(u'goto_actions', prompt=_(u'Goto actions'))
    goto_entries_menu.add_command(
        label=_(u'Go to workspace'), command=cmds.GotoWorkspaceCmd)
    bar_entries_menu = Menu('bar_actions', prompt=_(u'Bar actions'))
    scratchpad_entries_menu = Menu(
        u'scratchpad_actions', prompt=_(u'Scratchpad actions'))

    root_menu = Menu('root', prompt=_(u'Root'), root=True)
    root_menu.add_cascade(
        label=goto_entries_menu.prompt, menu=goto_entries_menu)
    root_menu.add_cascade(
        label=window_entries_menu.prompt, menu=window_entries_menu)
    root_menu.add_cascade(
        label=workspace_entries_menu.prompt, menu=workspace_entries_menu)
    root_menu.add_cascade(
        label=bar_entries_menu.prompt, menu=bar_entries_menu)
    root_menu.add_cascade(
        label=scratchpad_entries_menu.prompt, menu=scratchpad_entries_menu)
    root_menu.add_cascade(
        label=global_entries_menu.prompt, menu=global_entries_menu)
    return root_menu


class Application(object):
    __name__ = __name__

    def __init__(self, args=None):
        self.config = self.parse_args(args)
        self.i3 = I3Connector()
        self.mp = self.get_menu_provider()

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
        if self.config.get('debug'):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)
        if not self.mp:
            logger.info(u'No menu provider found. Testing?')
        self.tree = menu_tree()
        if self.config.get('root'):
            self.tree = menu_root(self.tree, self.config['root'])
            self.tree.root = True
            logger.info(u'Initial root: {root}'.format(root=self.tree))

    def run(self):
        self.apply_config()
        cmd_klass = mainloop(self.mp, self.tree)
        if not cmd_klass:
            logger.info(u'No valid choice made. Bye bye :)')
            sys.exit()
        cmd = cmd_klass()
        params = self.collect_command_params(cmd)
        if params is None:
            sys.exit()
        cmd_msg = cmd.cmd(**params)
        logger.info(u'Running i3 command: "{cmd}"'.format(cmd=cmd_msg))
        res = self.i3.command(cmd_msg)
        if not len(res):
            logger.info(u'The command made no changes on i3')
            return
        elif res[0].get('success'):
            logger.info(u'Done! Cheers, bye! :)')
            return
        else:
            return res[0].get('error')

    def collect_command_params(self, cmd):
        required_params = cmd.params()
        params = {}
        for p in required_params:
            if p.default:
                params[p.name] = p.default
            elif p.default_fnc:
                entry = display_menu(self.mp, p.fnc, filter_fnc=p.default_fnc)
                if not entry:
                    return None
                params[p.name] = entry.value
            else:
                entry = display_menu(self.mp, p.fnc)
                if not entry:
                    return None
                if isinstance(entry, six.string_types):
                    params[p.name] = entry
                else:
                    params[p.name] = entry.value
        return params

    def _bar_entries(self, filter_fnc=None):
        entries_list = self.conn.get_bar_ids()
        if len(entries_list) == 1:
            return entries_list[0]
        entries = [{'label': i, 'value': i} for i in sorted(entries_list)]
        return entries

    def get_menu_provider(self):
        cmd = None
        if self.config.get('menu_provider'):
            cmd = which(self.config.get('menu_provider'))
        elif which('rofi'):
            cmd = which('rofi')
        elif which('dmenu'):
            cmd = which('dmenu')
        return cmd


if __name__ == '__main__':
    app = Application()
    app.run()
