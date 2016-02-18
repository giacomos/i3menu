#!/usr/bin/env python
# -*- coding: utf-8 -*-
import i3
import subprocess

GO_BACK_OPTION = '<- go back'
GO_BACK_SIGNAL = '<go back>'
DEFAULT_TITLE = 'Select:'


class I3Rofi(object):

    def _rofi_menu(self, options, title='Select'):
        cmd = 'echo "{options}" | rofi -dmenu -p "{title}"'.format(
            options='\n'.join(options),
            title=title
        )
        proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
        return proc.stdout.read().strip('\n')

    def _i3_get_all_workspaces(self):
        return i3.get_workspaces()

    def _i3_get_all_outputs(self):
        return i3.get_outputs()

    def _i3_get_focused_workspace(self):
        return i3.filter(tree=i3.get_workspaces(), focused=True)[0]

    def _i3_get_unfocused_workspaces(self):
        return i3.filter(tree=i3.get_workspaces(), focused=False)

    def _i3_get_active_outputs(self):
        return i3.filter(tree=i3.get_outputs(), active=True)

    def _i3_get_workspace_output(self, ws):
        active_outputs = self._i3_get_active_outputs()
        for o in active_outputs:
            cw = o['current_workspace']
            cw = cw and cw or []
            if ws['name'] in cw:
                return o

    def _i3_get_focused_output(self):
        ws = self._i3_get_focused_workspace()
        return self._i3_get_workspace_output(ws)

    def _i3_get_unfocused_outputs(self):
        active_outputs = self._i3_get_active_outputs()
        focused_output = self._i3_get_focused_output()
        active_outputs.pop(active_outputs.index(focused_output))
        return active_outputs

    def _rofi_select_workspace(self, title=DEFAULT_TITLE,
                               unfocused_only=True, submenu=False):
        ws_list = unfocused_only and self._i3_get_unfocused_workspaces() or \
            self._i3_get_all_workspaces()
        ws_names = sorted([i['name'] for i in ws_list])
        if submenu:
            ws_names = [GO_BACK_OPTION] + ws_names
        choice = self._rofi_menu(
            ws_names,
            title=title)
        return choice

    def _rofi_select_output(self, title=DEFAULT_TITLE,
                            unfocused_only=True, submenu=False):
        outputs_list = []
        if unfocused_only:
            outputs_list = self._i3_get_unfocused_outputs()
        else:
            outputs_list = self._i3_get_all_outputs()
        outputs_names = sorted([i['name'] for i in outputs_list])
        ordered_list = [
            '{idx}: {entry}'.format(idx=i + 1, entry=entry)
            for i, entry in enumerate(outputs_names)]
        if submenu:
            ordered_list = [GO_BACK_OPTION] + ordered_list
        choice = self._rofi_menu(
            ordered_list,
            title=title)
        return choice

    def go_to_workspace(self, submenu=False):
        choice = self._rofi_select_workspace(
            'Go to workspace:',
            submenu=submenu)
        if not choice or choice == GO_BACK_OPTION:
            return GO_BACK_SIGNAL
        return i3.workspace(choice)

    def move_window_to_workspace(self, submenu=False):
        choice = self._rofi_select_workspace(
            'Move focused window to workspace:',
            submenu=submenu)
        if not choice or choice == GO_BACK_OPTION:
            return GO_BACK_SIGNAL
        return i3.move('window to workspace "%s"' % choice)

    def move_workspace_to_output(self, submenu=False):
        choice = self._rofi_select_output(
            'Move active workspace to output:',
            submenu=submenu)
        if not choice or choice == GO_BACK_OPTION:
            return GO_BACK_SIGNAL
        return i3.move('workspace to output "%s"' % choice)

    def rename_workspace(self, submenu=False):
        ws = self._i3_get_focused_workspace()
        choice = self._rofi_menu([ws['name']], 'Rename workspace:')
        if not choice or choice == GO_BACK_OPTION:
            return GO_BACK_SIGNAL
        return i3.rename('workspace to "%s"' % choice)

    def move_window_to_this_workspace(self, submenu=False):
        wps = self._i3_get_all_workspaces()
        all_windows = []
        for wp in wps:
            workspace = i3.filter(num=wp['num'])
            if not workspace:
                continue
            workspace = workspace[0]
            all_windows.extend(i3.filter(workspace, nodes=[]))
        window_classes = [w['window_properties']['class'] for w in all_windows]
        choice = self._rofi_menu(window_classes, 'Choose window:')
        if not choice or choice == GO_BACK_OPTION:
            return GO_BACK_SIGNAL
        return i3.command(
            '[class="%s"] move window to workspace current' % choice)

    def window_actions(self):
        actions = {
            '1: Move to workspace ->': {
                'callback': self.move_window_to_workspace,
                'submenu': True
            },
            '2: Floating (toggle)': {
                'callback': lambda x: i3.floating('toggle'),
            },
            '3: Fullscreen (toggle)': {
                'callback': lambda x: i3.fullscreen(),
            },
            '4: Sticky (toggle)': {
                'callback': lambda x: i3.sticky('toggle'),
            },
            '5: Move to Scratchpad': {
                'callback': lambda x: i3.move('scratchpad'),
            },
            '5: Move window to this workspace': {
                'callback': self.move_window_to_this_workspace,
                'submenu': True
            },
            '6: Quit': {
                'callback': lambda x: i3.kill(),
            }
        }
        choice = self._rofi_menu(sorted(actions.keys()), 'Window actions:')
        if not choice:
            return
        callback = actions[choice]['callback']
        submenu = actions[choice].get('submenu', False)
        res = callback(submenu)
        if res == GO_BACK_SIGNAL:
            self.window_actions()
        return

    def workspace_actions(self):
        actions = {
            '1: Go to workspace ->': {
                'callback': self.go_to_workspace,
                'submenu': True
            },
            '2: Move workspace to output ->': {
                'callback': self.move_workspace_to_output,
                'submenu': True
            },
            '3: Rename workspace ->': {
                'callback': self.rename_workspace,
                'submenu': True
            },
        }
        choice = self._rofi_menu(sorted(actions.keys()), 'Workspace actions:')
        if not choice:
            return
        callback = actions[choice]['callback']
        submenu = actions[choice].get('submenu', False)
        res = callback(submenu)
        if res == GO_BACK_SIGNAL:
            self.workspace_actions()
        return
