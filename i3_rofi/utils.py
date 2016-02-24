# -*- coding: utf-8 -*-
import os
import sys
import errno
import subprocess
import i3ipc
import i18n

# Create the Connection object that can be used to send commands and subscribe
# to events.
i3 = i3ipc.Connection()

ROFI_PREFIX = '(i3-rofi)'

_ = i18n.language.gettext
DEFAULT_TITLE = _('Select:')


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


def safe_list_get(l, idx, default):
    try:
        idx = int(idx)
        return l[idx]
    except Exception, e:
        print e
        return default


def rofi(options, title=DEFAULT_TITLE, **kwargs):
    rofi_cmd = which('rofi')
    title = ' '.join([ROFI_PREFIX, title])
    safe_title = '"%s"' % title
    rofi_args = {'format': 'i'}
    rofi_args.update(kwargs)
    rofi_args_list = ['-dmenu', '-p', safe_title]
    for k,v in rofi_args.iteritems():
        rofi_args_list.append('-' + k)
        if isinstance(v, str):
            rofi_args_list.append(v)
        else:
            rofi_args_list.extend(list(v))
    cmd = 'echo "{options}" | {rofi} {rofi_args}'.format(
        rofi=rofi_cmd,
        rofi_args=' '.join(rofi_args_list),
        options='\n'.join(options),
        title=title,
    )
    proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    return proc.stdout.read().strip('\n')


def i3_get_workspaces():
    return i3.get_workspaces()


def i3_get_outputs():
    return i3.get_outputs()


def i3_get_windows():
    return i3.get_tree().leaves()


def i3_get_scratchpad_windows():
    return i3.get_tree().scratchpad().leaves()


def i3_get_focused_workspace():
    win = i3.get_tree().find_focused()
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


def i3_command(cmd, debug=False):
    if debug:
        print cmd
    i3.command(cmd)


def select(options, title=DEFAULT_TITLE):
    if len(options) == 1:
        return options[0]
    idx = rofi(options, title=title)
    option = safe_list_get(options, idx, None)
    if not option:
        sys.exit()
    return option


def select_bar(title=DEFAULT_TITLE, filter_fnc=None):
    entries_list = i3_get_bar_ids()
    options = sorted(entries_list)
    return select(options, title=title)


def select_workspace(title=DEFAULT_TITLE, filter_fnc=None):
    entries_list = i3_get_workspaces()
    entries_list = sorted(entries_list, key=lambda x: x.name)
    if filter_fnc:
        entries_list = [e for e in filter(filter_fnc, entries_list)]
    options = []
    for ws in entries_list:
        current = ws['focused'] and ' (current)' or ''
        label = '{name} {current}'.format(
            name=ws['name'], current=current)
        options.append(label)
    if len(options) == 1:
        idx = 0
    else:
        idx = rofi(options, title=title)
    ws = safe_list_get(entries_list, idx, None)
    if not ws:
        sys.exit()
    return ws


def select_output(title=DEFAULT_TITLE, filter_fnc=None):
    entries_list = i3_get_active_outputs()
    entries_list = sorted(entries_list, key=lambda x: x.get('name'))
    if filter_fnc:
        entries_list = [e for e in filter(filter_fnc, entries_list)]
    options = []
    focused_output = i3_get_focused_output()
    for i, out in enumerate(entries_list):
        current = out['name'] == focused_output \
            and '(current)' or ''
        label = '{idx}: {name} {current}'.format(
            idx=i, name=out['name'], current=current)
        options.append(label)
    if len(options) == 1:
        idx = 0
    else:
        idx = rofi(options, title=title)
    ws = safe_list_get(entries_list, idx, None)
    if not ws:
        sys.exit()
    return ws


def select_window(title=DEFAULT_TITLE, scratchpad=False):
    entries = []
    entries_list = i3_get_windows()
    if scratchpad:
        entries_list = i3_get_scratchpad_windows()
    for win in entries_list:
        entry = '{winclass}\t{title}'.format(
            winclass=win.window_class.encode('utf-8'),
            title=win.name.encode('utf-8'))
        entries.append(entry)
    options = [
        '{idx}: {entry}'.format(idx=i + 1, entry=e)
        for i, e in enumerate(entries)]
    if len(options) == 1:
        idx = 0
    else:
        idx = rofi(options, title=title)
    ws = safe_list_get(entries_list, idx, None)
    if not ws:
        sys.exit()
    return ws
