# -*- coding: utf-8 -*-
import i3ipc
import subprocess
import sys
from i3menu import _
from i3menu import logger
from i3menu.utils import which
from i3menu.utils import iteritems

PROMPT_PREFIX = '(i3menu)'
DEFAULT_TITLE = _('Select:')

i3 = i3ipc.Connection()


class FakeOutput(object):
    name = ''

    def __init__(self, name):
        self.name = name

xrandr_directions = [
    FakeOutput(u'left'),
    FakeOutput(u'right'),
    FakeOutput(u'up'),
    FakeOutput(u'down'),
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


def select_bar(title=DEFAULT_TITLE, filter_fnc=None, context=None):
    entries_list = i3_get_bar_ids()
    if len(entries_list) == 1:
        return entries_list[0]
    options = {i: i for i in sorted(entries_list)}
    return menu(options, title=title, context=context)


def select_workspace(title=DEFAULT_TITLE, filter_fnc=None, context=None):
    entries_list = i3_get_workspaces()
    entries_list = sorted(entries_list, key=lambda x: x.name)
    if filter_fnc:
        entries_list = [e for e in filter(filter_fnc, entries_list)]
    options = {}
    for ws in entries_list:
        current = ws['focused'] and ' (current)' or ''
        label = '{name} {current}'.format(
            name=ws['name'], current=current)
        options[label] = ws
    if len(options.keys()) == 1:
        return options.values()[0]
    else:
        return menu(options, title=title, context=context)


def select_output(title=DEFAULT_TITLE, filter_fnc=None, context=None):
    entries_list = i3_get_active_outputs()
    entries_list = sorted(entries_list, key=lambda x: x.get('name'))
    entries_list = xrandr_directions + entries_list
    if filter_fnc:
        entries_list = [e for e in filter(filter_fnc, entries_list)]
    options = {}
    focused_output = i3_get_focused_output()
    for i, out in enumerate(entries_list):
        name = isinstance(out, FakeOutput) and '<%s>' % out.name or out.name
        name += out.name == focused_output.name \
            and ' (current)' or ''
        label = '{idx}: {name}'.format(
            idx=i, name=name)
        options[label] = out
    if len(options.keys()) == 1:
        return options.values()[0]
    else:
        return menu(options, title=title, context=context)


def select_window(title=DEFAULT_TITLE, scratchpad=False, context=None):
    entries = []
    entries_list = i3_get_windows()
    if scratchpad:
        entries_list = i3_get_scratchpad_windows()
    for win in entries_list:
        entry = '{winclass}\t{title}'.format(
            winclass=win.window_class.encode('utf-8'),
            title=win.name.encode('utf-8'))
        entries.append(entry)
    options = {
        '{idx}: {entry}'.format(idx=i + 1, entry=e): e
        for i, e in enumerate(entries)}
    if len(options.keys()) == 1:
        return options.values()[0]
    else:
        return menu(options, title=title, context=context)
