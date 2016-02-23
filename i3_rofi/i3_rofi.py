# -*- coding: utf-8 -*-
import sys
import errno
import i3
import subprocess
from utils import which
from utils import safe_list_get
from utils import rofi
import i18n

GO_BACK_OPTION = '<- go back'
GO_BACK_SIGNAL = '<go back>'
ROFI_PREFIX = '(i3-rofi)'

_ = i18n.language.gettext
DEFAULT_TITLE = _('Select:')


class I3Rofi(object):

    def check_rofi(self):
        '''Check if rofi is available.'''
        if which('rofi'):
            return True
        else:
            sys.exit(errno.EINVAL)

    def _i3_get_workspaces(self):
        return i3.get_workspaces()

    def _i3_get_outputs(self):
        return i3.get_outputs()

    def _i3_get_windows(self):
        return i3.filter(**{'nodes': [], 'type': 'con'})

    def _i3_get_focused_workspace(self):
        return i3.filter(tree=i3.get_workspaces(), focused=True)[0]

    def _i3_get_unfocused_workspaces(self):
        return i3.filter(tree=i3.get_workspaces(), focused=False)

    def _i3_get_active_outputs(self):
        return i3.filter(tree=i3.get_outputs(), active=True)

    def _i3_get_focused_output(self):
        ws = self._i3_get_focused_workspace()
        return ws['output']

    def _i3_get_unfocused_outputs(self):
        active_outputs = self._i3_get_active_outputs()
        focused_output = self._i3_get_focused_output()
        active_outputs.pop(active_outputs.index(focused_output))
        return active_outputs

    def _select_workspace(self, title=DEFAULT_TITLE):
        entries_list = self._i3_get_workspaces()
        entries_list = sorted(entries_list, key=lambda x: x.get('name'))
        labels = []
        for ws in entries_list:
            current = ws['focused'] and ' (current)' or ''
            label = '{name} {current}'.format(
                name=ws['name'], current=current)
            labels.append(label)
        idx = rofi(labels, title=title)
        return safe_list_get(entries_list, idx, None)

    def _select_output(self, title=DEFAULT_TITLE,
                       unfocused_only=True):
        entries_list = self._i3_get_active_outputs()
        entries_list = sorted(entries_list, key=lambda x: x.get('name'))
        labels = []
        focused_output = self._i3_get_focused_output()
        for i, out in enumerate(entries_list):
            current = out['name'] == focused_output \
                and '(current)' or ''
            label = '{idx}: {name} {current}'.format(
                idx=i, name=out['name'], current=current)
            labels.append(label)
        idx = rofi(labels, title=title)
        return safe_list_get(entries_list, idx, None)

    def _select_window(self, title=DEFAULT_TITLE):
        entries = []
        entries_list = self._i3_get_windows()
        for win in entries_list:
            entry = '{winclass}\t{title}'.format(
                winclass=win['window_properties']['class'],
                title=win['name'].encode('utf-8'))
            entries.append(entry)
        ordered_list = [
            '{idx}: {entry}'.format(idx=i + 1, entry=e)
            for i, e in enumerate(entries)]
        idx = rofi(
            ordered_list,
            title=title)
        return safe_list_get(entries_list, idx, None)

    def go_to_workspace(self, debug=False):
        ws = self._select_workspace(_('Go to workspace:'))
        if not ws:
            return GO_BACK_SIGNAL
        if debug:
            print 'i3-msg workspaces "{ws}"'.format(ws=ws.get('name'))
        return i3.workspace(ws.get('name'))

    def move_window_to_workspace(self, debug=False):
        ws = self._select_workspace(_('Move window to workspace:'))
        if not ws:
            return GO_BACK_SIGNAL
        CMD = 'window to workspace "{ws}"'.format(ws=ws.get('name'))
        if debug:
            print CMD
        return i3.move(CMD)

    def move_workspace_to_output(self, debug=False):
        out = self._select_output(_('Move active workspace to output:'))
        if not out:
            return GO_BACK_SIGNAL
        CMD = 'workspace to output "{output}"'.format(output=out.get('name'))
        if debug:
            print CMD
        return i3.move(CMD)

    def rename_workspace(self, debug=False):
        ws = self._i3_get_focused_workspace()
        choice = rofi(
            [ws['name']], _('Rename workspace:'), **{'format': 's'})
        if not choice or choice == GO_BACK_OPTION:
            return GO_BACK_SIGNAL
        CMD = 'workspace to "{output}"'.format(output=choice)
        if debug:
            print CMD
        return i3.rename(CMD)

    def move_window_to_this_workspace(self, debug=False):
        win = self._select_window(
            _('Select a window to move to this workspace:'))
        if not win:
            return GO_BACK_SIGNAL
        CMD = '[class="{winclass}"] move window to workspace current'.format(
            winclass=win['window_properties']['class'])
        if debug:
            print CMD
        return i3.command(CMD)

    def window_actions(self, debug=False):
        actions = [
            {'title': _('Move window to workspace:'),
             'callback': self.move_window_to_workspace},
            {'title': _('Floating (toggle)'),
             'callback': lambda x: i3.floating('toggle')},
            {'title': _('Fullscreen (toggle)'),
             'callback': lambda x: i3.fullscreen()},
            {'title': _('Sticky (toggle)'),
             'callback': lambda x: i3.sticky('toggle')},
            {'title': _('Move to Scratchpad'),
             'callback': lambda x: i3.move('scratchpad')},
            {'title': _('Move window to this workspace'),
             'callback': self.move_window_to_this_workspace},
            {'title': _('Quit'),
             'callback': lambda x: i3.kill()}
        ]
        entries = [
            '%s: %s' % (idx + 1, i['title'])
            for idx,i in enumerate(actions)]
        idx = rofi(entries, _('Window actions:'))
        action = safe_list_get(actions, idx, None)
        callback = action['callback']
        res = callback(debug=debug)
        if res == GO_BACK_SIGNAL:
            self.window_actions()
        return

    def workspace_actions(self, debug=True):
        actions = [
            {'title': _('Go to workspace:'),
             'callback': self.go_to_workspace},
            {'title': _('Move active workspace to output:'),
             'callback': self.move_workspace_to_output},
            {'title': _('Rename workspace:'),
             'callback': self.rename_workspace},
            {'title': _('Move window to this workspace:'),
             'callback': self.move_window_to_this_workspace},
        ]
        entries = [
            '%s: %s' % (idx + 1, i['title'])
            for idx,i in enumerate(actions)]
        idx = rofi(entries, _('Workspace actions:'))
        action = safe_list_get(actions, idx, None)
        callback = action['callback']
        res = callback()
        if res == GO_BACK_SIGNAL:
            self.workspace_actions()
        return

    @property
    def menus(self):
        menus = [
            'go_to_workspace',
            'move_window_to_workspace',
            'move_window_to_this_workspace',
            'move_workspace_to_output',
            'rename_workspace',
            'window_actions',
            'workspace_actions',
        ]
        return menus

    def run(self, cli_args):
        self.check_rofi()
        if cli_args.menu not in self.menus:
            sys.exit(errno.EINVAL)
        menu_fnc = getattr(self, cli_args.menu)
        menu_fnc(debug=cli_args.debug)
