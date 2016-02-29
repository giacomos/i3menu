# -*- coding: utf-8 -*-
import i3ipc
import subprocess
import sys
from collections import OrderedDict
from i3menu import _
from i3menu import logger
from i3menu.utils import which
from i3menu.utils import iteritems

PROMPT_PREFIX = '(i3menu)'
DEFAULT_TITLE = _('Select:')
LABEL_GENERIC = '{idx}: {entry}'
LABEL_WINDOW = '{idx}: {window_class}\t{name}'
LABEL_OUTPUT = '{idx}: {name}{current}'
LABEL_WORKSPACE = '{name}{current}'

i3 = i3ipc.Connection()

XRANDR_DIRECTION_LEFT = {'name': u'left'}
XRANDR_DIRECTION_RIGHT = {'name': u'right'}
XRANDR_DIRECTION_UP = {'name': u'up'}
XRANDR_DIRECTION_DOWN = {'name': u'down'}

XRANDR_DIRECTIONS = [
    XRANDR_DIRECTION_LEFT,
    XRANDR_DIRECTION_RIGHT,
    XRANDR_DIRECTION_UP,
    XRANDR_DIRECTION_DOWN
]


def i3_get_workspaces():
    return i3.get_workspaces()


def i3_get_outputs():
    return i3.get_outputs()


def i3_get_windows():
    return i3.get_tree().leaves()


def i3_get_window():
    return i3.get_tree().find_focused()


def i3_get_scratchpad_windows():
    return i3.get_tree().scratchpad().leaves()


def i3_get_focused_workspace():
    win = i3_get_window()
    return win.workspace()


def i3_get_active_outputs():
    outputs = i3.get_outputs()
    return [o for o in filter(lambda o: o.active, outputs)]


def i3_get_focused_output():
    ws = i3_get_focused_workspace()
    out = ws.parent.parent
    return out


def i3_get_unfocused_outputs():
    active_outputs = i3_get_active_outputs()
    focused_output = i3_get_focused_output()
    active_outputs.pop(active_outputs.index(focused_output))
    return active_outputs


def i3_get_bar_ids():
    return i3.get_bar_config_list()


def i3_command(cmd, context=None):
    if context and context.get('debug'):
        logger.info(cmd)
    res = i3.command(cmd)
    return res


def _menu(cmd, options, title=DEFAULT_TITLE, context=None):
    title = ' '.join([PROMPT_PREFIX, title])
    safe_title = '"%s"' % title
    # cmd_args = {'format': 'i'}
    cmd_args = {}
    cmd_args_list = ['-p', safe_title]
    if 'rofi' in cmd:
        cmd_args_list = ['-dmenu'] + cmd_args_list
    for k, v in iteritems(cmd_args):
        cmd_args_list.append('-' + k)
        if isinstance(v, str):
            cmd_args_list.append(v)
        else:
            cmd_args_list.extend(list(v))
    cmd = 'echo "{options}" | {cmd} {cmd_args}'.format(
        cmd=cmd,
        cmd_args=' '.join(cmd_args_list),
        options='\n'.join(options),
        title=title,
    )
    if context and context.get('debug'):
        print cmd
    proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    label = proc.stdout.read().decode('utf-8').strip('\n')
    return options.get(label)


def menu(options, title=DEFAULT_TITLE, context=None):
    cmd = None
    if context and context.get('menu_provider'):
        cmd = which(context.get('menu_provider'))
    elif which('rofi'):
        cmd = which('rofi')
    elif which('dmenu'):
        cmd = which('dmenu')
    else:
        sys.exit('Either dmenu or rofi commands are required')
    return _menu(cmd, options, title=title, context=context)


def select(entries, title=DEFAULT_TITLE, context=None):
    options = OrderedDict()
    idx = 1
    for k, v in iteritems(entries):
        params = {}
        params['idx'] = idx
        params['entry'] = k
        label = LABEL_GENERIC.format(**params)
        options[label] = v
        idx += 1
    return menu(options, title=title, context=context)


def select_bar(title=DEFAULT_TITLE, filter_fnc=None, context=None):
    entries_list = i3_get_bar_ids()
    if len(entries_list) == 1:
        return entries_list[0]
    options = OrderedDict()
    for i in sorted(entries_list):
        options[i] = i
    return menu(options, title=title, context=context)


def select_workspace(title=DEFAULT_TITLE, filter_fnc=None, context=None):
    workspaces = i3_get_workspaces()
    workspaces = sorted(workspaces, key=lambda x: x.name)
    if filter_fnc:
        workspaces = [e for e in filter(filter_fnc, workspaces)]
    if len(workspaces) == 1:
        return workspaces[0]
    options = OrderedDict()
    for i, ws in enumerate(workspaces):
        params = ws.copy()
        params['idx'] = i + 1
        params['current'] = ws['focused'] and ' (current)' or ''
        label = LABEL_WORKSPACE.format(**params)
        options[label] = ws
    return menu(options, title=title, context=context)


def select_output(title=DEFAULT_TITLE, filter_fnc=None, context=None):
    outputs = i3_get_active_outputs()
    outputs = sorted(outputs, key=lambda x: x.get('name'))
    outputs = XRANDR_DIRECTIONS + outputs
    if filter_fnc:
        outputs = [e for e in filter(filter_fnc, outputs)]
    if len(outputs) == 1:
        return outputs[0]
    options = OrderedDict()
    focused_output = i3_get_focused_output()
    for i, out in enumerate(outputs):
        params = out.copy()
        params['idx'] = i + 1
        params['current'] = out.get('name') == focused_output.name \
            and ' (current)' or ''
        label = LABEL_OUTPUT.format(**params)
        options[label] = out
    return menu(options, title=title, context=context)


def select_window(title=DEFAULT_TITLE, scratchpad=False, context=None):
    wins = i3_get_windows()
    if scratchpad:
        wins = i3_get_scratchpad_windows()
    wins = sorted(wins, key=lambda x: x.window_class)
    if len(wins) == 1:
        return wins[0]
    options = OrderedDict()
    current_win = i3_get_window()
    for i, win in enumerate(wins):
        params = {
            'window_class': win.window_class.encode('utf-8'),
            'name': win.name.encode('utf-8'),
            'idx': i + 1,
            'type': win.type,
            'window': win.window,
            'window_instance': win.window_instance,
            'current': win == current_win and ' (current)' or ''
        }
        label = LABEL_WINDOW.format(**params)
        options[label] = win
    return menu(options, title=title, context=context)
