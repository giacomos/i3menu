# -*- coding: utf-8 -*-
import sys
import subprocess
from i3menu.connector import I3Connector
from i3menu.utils import which
from i3menu.config import DEFAULTS
from i3menu.config import SUBMENU_SIGN
from i3menu.config import MENUENTRY_SIGN
from i3menu import _
from i3menu import logger
from i3menu import cmds
from i3menu.menu import Menu
from i3menu.menu import MenuEntry


class Application(object):
    __name__ = 'i3menu'

    def __init__(self, args=None):
        self.config = self.parse_args(args)
        self.i3 = I3Connector()
        self.mp = self.get_menu_provider()
        if not self.mp:
            logger.info('No menu provider found. Testing?')

    def parse_args(self, params=None):
        config = DEFAULTS
        if not params:
            return config
        if params.debug:
            config['debug'] = True
        if params.menu_provider:
            config['menu_provider'] = params.menu_provider
        # if params.action:
        #     config['action'] = params.action
        if params.label_workspace_format:
            config['label_workspace'] = params.label_workspace_format.decode()
        if params.label_output_format:
            config['label_output'] = params.label_output_format.decode()
        if params.label_window_format:
            config['label_window'] = params.label_window_format.decode()
        if params.menu:
            config['root'] = params.menu
        return config

    def run(self):
        tree = self._menu_tree()
        if self.config['root']:
            tree = self._menu_root(tree, self.config['root'])
            tree.root = True
        logger.info('Initial root: {root}'.format(root=tree))
        cmd_klass = self.display_menu(tree)
        if not cmd_klass:
            sys.exit()
        cmd = cmd_klass()
        params = self.collect_command_params(cmd)
        if params is None:
            sys.exit()
        cmd_msg = cmd.cmd(**params)
        logger.info('i3 command: "{cmd}"'.format(cmd=cmd_msg))
        self.i3.command(cmd_msg)

    def collect_command_params(self, cmd):
        required_params = cmd.params()
        params = {}
        for p in required_params:
            if p.default:
                params[p.name] = p.default
            elif p.default_fnc:
                entry = self.display_menu(p.fnc, filter_fnc=p.default_fnc)
                if not entry:
                    return None
                params[p.name] = entry
            else:
                entry = self.display_menu(p.fnc)
                if not entry:
                    return None
                params[p.name] = entry
        return params

    def display_menu(self, menu, filter_fnc=None):
        entry = self._display_menu(menu, filter_fnc=filter_fnc)
        if not entry:
            return None
        elif isinstance(entry, unicode):
            return entry
        elif isinstance(entry.value, Menu):
            newmenu = entry.value
            if not newmenu.root:
                newmenu.parent = menu
            return self.display_menu(newmenu)
        elif entry:
            return entry.value
        return None

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

    def _display_menu(self, menu, prompt=None, filter_fnc=None):
        entries = menu.entries
        if filter_fnc:
            entries = [e for e in filter(filter_fnc, entries)]
        if len(entries) == 1:
            logger.info('This menu has just one option, no need to diplay it')
            return entries[0]
        prompt = ' '.join([self.config.get('prompt_prefix'), menu.prompt])
        safe_prompt = '"%s": ' % prompt
        cmd_args = {}
        cmd_args_list = ['-p', safe_prompt]
        if 'rofi' in self.mp:
            cmd_args_list = ['-dmenu'] + cmd_args_list
        for k in cmd_args:
            v = cmd_args[k]
            cmd_args_list.append('-' + k)
            if isinstance(v, str):
                cmd_args_list.append(v)
            else:
                cmd_args_list.extend(list(v))
        safe_labels = []
        for i, e in enumerate(entries):
            icon = e.cascade and SUBMENU_SIGN or MENUENTRY_SIGN
            label = '{idx}: {label}{icon}'.format(
                idx=i,
                label=e.label.encode('utf-8'),
                icon=icon.encode('utf-8'))
            safe_labels.append(label)
        cmd = 'echo "{options}" | {cmd} {cmd_args}'.format(
            cmd=self.mp,
            cmd_args=' '.join(cmd_args_list),
            options='\n'.join(safe_labels),
            prompt=prompt,
        )
        if self.config.get('debug'):
            print(cmd)
        proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
        res = proc.stdout.read().decode('utf-8').strip('\n')
        res = res.strip(SUBMENU_SIGN).strip(MENUENTRY_SIGN).split(': ', 1)[-1]
        if len(entries) == 0:
            return res
        for e in entries:
            if e.label == res:
                return e

    def _menu_tree(self):

        window_entries_menu = Menu(
            'window_actions', prompt=_('Window Actions'))
        window_entries_menu.add_command(
            label=_('Move window to workspace'),
            command=cmds.MoveWindowToWorkspaceCmd)
        window_entries_menu.add_command(
            label=_('Border style'), command=cmds.BorderCmd)
        window_entries_menu.add_command(
            label=_('Split'), command=cmds.SplitCmd)
        window_entries_menu.add_command(
            label=_('Floating (toggle)'), command=cmds.FloatingCmd)
        window_entries_menu.add_command(
            label=_('Fullscreen (toggle)'), command=cmds.FullscreenCmd)
        window_entries_menu.add_command(
            label=_('Sticky'), command=cmds.StickyCmd)
        window_entries_menu.add_command(
            label=_('Move to Scratchpad'),
            command=cmds.MoveWindowToScratchpadCmd)
        window_entries_menu.add_command(
            label=_('Kill'), command=cmds.KillCmd)

        workspace_entries_menu = Menu(
            'workspace_actions', prompt=_('Workspace Actions'))
        workspace_entries_menu.add_command(
            label=_('Rename'),
            command=cmds.RenameWorkspaceCmd)
        workspace_entries_menu.add_command(
            label=_('Layout'),
            command=cmds.LayoutCmd)
        workspace_entries_menu.add_command(
            label=_('Move workspace to output'),
            command=cmds.MoveWorkspaceToOutputCmd)

        global_entries_menu = Menu(
            'global_actions', prompt=_("Global actions"))
        global_entries_menu.add_command(
            label=_('Debug log'), command=cmds.DebuglogCmd)
        global_entries_menu.add_command(
            label=_('Shared memory log'), command=cmds.ShmlogCmd)
        global_entries_menu.add_command(
            label=_('Restart i3'), command=cmds.RestartCmd)
        global_entries_menu.add_command(
            label=_('Reload i3'), command=cmds.ReloadCmd)
        global_entries_menu.add_command(
            label=_('Exit i3'), command=cmds.ExitCmd)

        goto_entries_menu = Menu('goto_actions', prompt=_("Goto actions"))
        goto_entries_menu.add_command(
            label=_('Go to workspace'), command=cmds.GotoWorkspaceCmd)

        root_menu = Menu('root', prompt='Root', root=True)
        root_menu.add_cascade(
            label=_('Goto actions'), menu=goto_entries_menu)
        root_menu.add_cascade(
            label=_('Window actions'), menu=window_entries_menu)
        root_menu.add_cascade(
            label=_('Workspace actions'), menu=workspace_entries_menu)
        root_menu.add_cascade(
            label=_('Bar actions'), menu='CIAO')
        root_menu.add_cascade(
            label=_('Scratchpad actions'), menu='CIAO')
        root_menu.add_cascade(
            label=_('Global actions'), menu=global_entries_menu)
        return root_menu

    def _menu_root(self, tree, root_name):
        menus_list = self._recursive_menu_traverse(tree)
        res = None
        for m in menus_list:
            if m.name == root_name:
                res = m
        if res:
            return res
        else:
            return tree

    def _recursive_menu_traverse(self, menu, results=None):
        results = results or []
        if isinstance(menu, Menu):
            results.append(menu)
            for child in menu.entries:
                if isinstance(child, MenuEntry) and \
                        isinstance(child.value, Menu):
                    results.extend(
                        self._recursive_menu_traverse(child.value, results))
        return results

if __name__ == '__main__':
    app = Application()
    app.run()
