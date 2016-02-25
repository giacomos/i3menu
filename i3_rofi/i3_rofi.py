# -*- coding: utf-8 -*-
import sys
import errno
from .utils import which
from .utils import safe_list_get
from . import api
from . import _

COMMANDS_ACTIONS = {
    'sticky': [
        'enable', 'disable', 'toggle'],
    'fullscreen': [
        'enable', 'disable', 'toggle'],
    'floating': [
        'enable', 'disable', 'toggle'],
    'bar_hidden_state': [
        'hide', 'show', 'toggle'],
    'bar_mode': [
        'dock', 'hide', 'invisible', 'toggle'],
    'layout': [
        'default', 'tabbed', 'stacking', 'splitv', 'splith']
}


class I3Rofi(object):
    menus = [
        'go_to_workspace',
        'move_window_to_workspace',
        'move_window_to_this_workspace',
        'move_workspace_to_output',
        'rename_workspace',
        'window_actions',
        'workspace_actions',
        'scratchpad_actions',
        'bar_actions',
        'layout',
    ]

    def __init__(self, menu, debug=False):
        if menu not in self.menus:
            sys.exit(errno.EINVAL)
        self.menu_fnc = getattr(self, menu)
        self.debug = debug

    def __call__(self):
        self.check_rofi()
        self.menu_fnc()

    def check_rofi(self):
        '''Check if rofi is available.'''
        if which('rofi'):
            return True
        else:
            sys.exit(errno.EINVAL)

    def go_to_workspace(self, debug=False):
        ws = api.rofi_select_workspace(_('Go to workspace:'))
        cmd = 'workspace "{ws}"'.format(ws=ws.name)
        return api.i3_command(cmd, debug=debug)

    def move_window_to_workspace(self, debug=False):
        ws = api.rofi_select_workspace(_('Move window to workspace:'))
        cmd = 'move window to workspace "{ws}"'.format(ws=ws.name)
        return api.i3_command(cmd, debug=debug)

    def move_workspace_to_output(self, debug=False):
        out = api.rofi_select_output(_('Move active workspace to output:'))
        cmd = 'move workspace to output "{output}"'.format(output=out.name)
        return api.i3_command(cmd, debug=debug)

    def rename_workspace(self, debug=False):
        ws = api.rofi_select_workspace(filter_fnc=lambda x: x.focused)
        choice = api._rofi(
            [ws.name.encode('utf-8')],
            _('Rename workspace:'),
            **{'format': 's'}
        )
        if not choice:
            return
        cmd = 'rename workspace to "{output}"'.format(output=choice)
        return api.i3_command(cmd, debug=debug)

    def move_window_to_this_workspace(self, debug=False):
        win = api.rofi_select_window(
            _('Select a window to move to this workspace:'))
        cmd = '[id="{id}"] move window to workspace current'.format(
            id=win.window)
        return api.i3_command(cmd, debug=debug)

    def floating(self, action=None, debug=False):
        """ http://i3wm.org/docs/userguide.html#_manipulating_layout
        """
        actions = COMMANDS_ACTIONS['floating']
        if not action or action not in actions:
            action = api.rofi_select(actions, title='action:')
        cmd = 'floating {action}'.format(action=action)
        return api.i3_command(cmd, debug=debug)

    def fullscreen(self, action=None, debug=False):
        """ http://i3wm.org/docs/userguide.html#_manipulating_layout
        """
        actions = COMMANDS_ACTIONS['fullscreen']
        if not action or action not in actions:
            action = api.rofi_select(actions, title='action:')
        cmd = 'fullscreen {action}'.format(action=action)
        return api.i3_command(cmd, debug=debug)

    def sticky(self, action=None, debug=False):
        """ http://i3wm.org/docs/userguide.html#_sticky_floating_windows
        """
        actions = COMMANDS_ACTIONS['sticky']
        if not action or action not in actions:
            action = api.rofi_select(actions, title='action:')
        cmd = 'sticky {action}'.format(action=action)
        return api.i3_command(cmd, debug=debug)

    def kill(self, debug=False):
        cmd = 'kill'
        return api.i3_command(cmd, debug=debug)

    def move_to_scratchpad(self, debug=False):
        cmd = 'move to scratchpad'
        return api.i3_command(cmd, debug=debug)

    def scratchpad_show(self, debug=False):
        win = api.rofi_select_window(
            _('Select a window to show:'),
            scratchpad=True)
        cmd = '[id="{id}"] scratchpad show'.format(id=win.window)
        return api.i3_command(cmd, debug=debug)

    def bar_hidden_state(self, action=None, debug=False):
        """ http://i3wm.org/docs/userguide.html#_i3bar_control
        """
        bar_id = api.rofi_select_bar(_('Select bar:'))
        actions = COMMANDS_ACTIONS['bar_hidden_state']
        if not action or action not in actions:
            action = api.rofi_select(actions, title='action:')
        cmd = 'bar hidden_state {action} "{bar_id}"'.format(
            action=action, bar_id=bar_id)
        return api.i3_command(cmd, debug=debug)

    def bar_mode(self, action=None, debug=False):
        """ http://i3wm.org/docs/userguide.html#_i3bar_control
        """
        bar_id = api.rofi_select_bar(_('Select bar:'))
        actions = COMMANDS_ACTIONS['bar_mode']
        if not action or action not in actions:
            action = api.rofi_select(actions, title='action:')
        cmd = 'bar mode {action} "{bar_id}"'.format(
            action=action, bar_id=bar_id)
        return api.i3_command(cmd, debug=debug)

    def layout(self, action=None, debug=False):
        """ http://i3wm.org/docs/userguide.html#_manipulating_layout
        """
        actions = COMMANDS_ACTIONS['layout']
        if not action or action not in actions:
            action = api.rofi_select(actions, title='action:')
        cmd = 'layout {action}'.format(action=action)
        return api.i3_command(cmd, debug=debug)

    def bar_actions(self, debug=False):
        """ http://i3wm.org/docs/userguide.html#_i3bar_control
        """
        actions = [
            {'title': _('hidden_state'),
             'callback': self.bar_hidden_state},
            {'title': _('mode'),
             'callback': self.bar_mode},
        ]
        entries = [
            '%s: %s' % (idx + 1, i['title'])
            for idx, i in enumerate(actions)]
        idx = api._rofi(entries, _('Bar actions:'))
        action = safe_list_get(actions, idx, None)
        callback = action['callback']
        callback(debug=debug)
        sys.exit()

    def scratchpad_actions(self, debug=False):
        """ http://i3wm.org/docs/userguide.html#_scratchpad
        """
        actions = [
            {'title': _('Move current window to scratchpad'),
             'callback': self.move_to_scratchpad},
            {'title': _('Show window from scratchpad'),
             'callback': self.scratchpad_show},
        ]
        entries = [
            '%s: %s' % (idx + 1, i['title'])
            for idx, i in enumerate(actions)]
        idx = api._rofi(entries, _('Window actions:'))
        action = safe_list_get(actions, idx, None)
        callback = action['callback']
        callback(debug=debug)
        sys.exit()

    def window_actions(self, debug=False):
        actions = [
            {'title': _('Move window to workspace:'),
             'callback': self.move_window_to_workspace},
            {'title': _('Floating (toggle)'),
             'callback': self.floating},
            {'title': _('Fullscreen (toggle)'),
             'callback': self.fullscreen},
            {'title': _('Sticky'),
             'callback': self.sticky},
            {'title': _('Move to Scratchpad'),
             'callback': self.move_to_scratchpad},
            {'title': _('Move window to this workspace'),
             'callback': self.move_window_to_this_workspace},
            {'title': _('Quit'),
             'callback': self.kill}
        ]
        entries = [
            '%s: %s' % (idx + 1, i['title'])
            for idx, i in enumerate(actions)]
        idx = api._rofi(entries, _('Window actions:'))
        action = safe_list_get(actions, idx, None)
        callback = action['callback']
        callback(debug=debug)
        sys.exit()

    def workspace_actions(self, debug=False):
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
            for idx, i in enumerate(actions)]
        idx = api._rofi(entries, _('Workspace actions:'))
        action = safe_list_get(actions, idx, None)
        callback = action['callback']
        callback(debug=debug)
        sys.exit()
