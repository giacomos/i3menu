# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from collections import OrderedDict
from i3menu.connector import I3Connector
from i3menu.config import XRANDR_DIRECTIONS


def which(program):
    """ check if an program exists and returns the path
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

try:
    dict.iteritems
except AttributeError:
    # Python 3
    def itervalues(d):
        return iter(d.values())

    def iteritems(d):
        return iter(d.items())
else:
    # Python 2
    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()


def _menu(cmd, options, prompt=None, config=None):
    if not prompt:
        prompt = config.get('prompt')
    prompt = ' '.join([config.get('prompt_prefix'), prompt])
    safe_prompt = '"%s"' % prompt
    cmd_args = {}
    cmd_args_list = ['-p', safe_prompt]
    if 'rofi' in cmd:
        cmd_args_list = ['-dmenu'] + cmd_args_list
    for k, v in iteritems(cmd_args):
        cmd_args_list.append('-' + k)
        if isinstance(v, str):
            cmd_args_list.append(v)
        else:
            cmd_args_list.extend(list(v))
    safe_options = '\n'.join([o.encode('utf-8') for o in options])
    cmd = 'echo "{options}" | {cmd} {cmd_args}'.format(
        cmd=cmd,
        cmd_args=' '.join(cmd_args_list),
        options=safe_options,
        prompt=prompt,
    )
    if config and config.get('debug'):
        print(cmd)
    proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    label = proc.stdout.read().decode('utf-8').strip('\n')
    return options.get(label)


def menu(options, prompt=None, config=None):
    """
        @options a dict {'label of the option': value to return}
    """
    cmd = None
    if not prompt:
        prompt = config.get('prompt')
    if len(options.keys()) == 0:
        return None
    elif len(options.keys()) == 1:
        return options.values()[0]
    if config and config.get('menu_provider'):
        cmd = which(config.get('menu_provider'))
    elif which('rofi'):
        cmd = which('rofi')
    elif which('dmenu'):
        cmd = which('dmenu')
    else:
        sys.exit('Either dmenu or rofi commands are required')
    return _menu(cmd, options, prompt=prompt, config=config)


def select(entries, prompt=None, filter_fnc=None, config=None):
    options = OrderedDict()
    idx = 1
    if filter_fnc:
        tmp = [e for e in filter(filter_fnc, entries)]
        entries = tmp
    for k, v in iteritems(entries):
        params = {}
        params['idx'] = idx
        params['entry'] = k
        label = config.get('label_generic').format(**params)
        options[label] = v
        idx += 1
    return menu(options, prompt=prompt, config=config)


def select_bar(prompt=None, filter_fnc=None, config=None):
    conn = I3Connector(config=config)
    entries_list = conn.get_bar_ids()
    if len(entries_list) == 1:
        return entries_list[0]
    options = OrderedDict()
    for i in sorted(entries_list):
        options[i] = i
    return menu(options, prompt=prompt, config=config)


def select_workspace(prompt=None, filter_fnc=None, config=None):
    conn = I3Connector(config=config)
    workspaces = conn.get_workspaces()
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
        label = config.get('label_workspace').format(**params)
        options[label] = ws
    return menu(options, prompt=prompt, config=config)


def select_output(prompt=None, filter_fnc=None, config=None):
    conn = I3Connector(config=config)
    outputs = conn.get_active_outputs()
    outputs = sorted(outputs, key=lambda x: x.get('name'))
    outputs = XRANDR_DIRECTIONS + outputs
    if filter_fnc:
        tmp = [e for e in filter(filter_fnc, outputs)]
        outputs = tmp
    if len(outputs) == 1:
        return outputs[0]
    options = OrderedDict()
    focused_output = conn.get_focused_output()
    for i, out in enumerate(outputs):
        params = out.copy()
        params['idx'] = i + 1
        params['current'] = out.get('name') == focused_output.name \
            and ' (current)' or ''
        label = config.get('label_output').format(**params)
        options[label] = out
    return menu(options, prompt=prompt, config=config)


def select_window(prompt=None, filter_fnc=None, scratchpad=False, config=None):
    conn = I3Connector(config=config)
    wins = conn.get_windows()
    if scratchpad:
        wins = conn.get_scratchpad_windows()
    wins = sorted(wins, key=lambda x: x.window_class)
    if filter_fnc:
        tmp = [e for e in filter(filter_fnc, wins)]
        wins = tmp
    if len(wins) == 1:
        return wins[0]
    options = OrderedDict()
    for i, win in enumerate(wins):
        params = {'idx': i + 1, 'window': win}
        label = config.get('label_window').format(**params)
        options[label] = win
    return menu(options, prompt=prompt, config=config)
