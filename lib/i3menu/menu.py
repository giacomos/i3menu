# -*- coding: utf-8 -*-
import six
import subprocess

from i3menu import _
from i3menu import logger
from i3menu import __name__
from i3menu.config import SUBMENU_SIGN
from i3menu.config import MENUENTRY_SIGN
from i3menu.config import LABEL_WINDOW
from i3menu.config import LABEL_WORKSPACE
from i3menu.config import LABEL_OUTPUT
from i3menu.connector import I3Connector
from i3menu.utils import safe_decode
from i3menu.utils import safe_join


class MenuEntry(object):

    label = u''
    value = None
    cascade = False

    def __init__(self, label=None, value=None, cascade=False):
        if label:
            self.label = label
        self.value = value
        self.cascade = cascade


class DummyOutput(object):
    name = None

    def __init__(self, name):
        self.name = name


XRANDR_DIRECTION_LEFT = MenuEntry(**{
    'label': u'<left>', 'value': DummyOutput('left')})
XRANDR_DIRECTION_RIGHT = MenuEntry(**{
    'label': u'<right>', 'value': DummyOutput('right')})
XRANDR_DIRECTION_UP = MenuEntry(**{
    'label': u'<up>', 'value': DummyOutput('up')})
XRANDR_DIRECTION_DOWN = MenuEntry(**{
    'label': u'<down>', 'value': DummyOutput('down')})

XRANDR_DIRECTIONS = [
    XRANDR_DIRECTION_LEFT,
    XRANDR_DIRECTION_RIGHT,
    XRANDR_DIRECTION_UP,
    XRANDR_DIRECTION_DOWN
]


class Menu(object):
    name = 'root'
    prompt = u'Menu'
    _entries = None
    parent = None
    root = False
    start_idx = 1
    filter_fnc = None

    def __init__(
            self, name, prompt=None, entries=None, parent=None, start_idx=1,
            filter_fnc=None, root=False):
        self.name = name
        if prompt:
            self.prompt = prompt
        self._entries = entries and entries or []
        self.parent = parent
        self.start_idx = start_idx
        self.root = root
        self.filter_fnc = filter_fnc

    def add_command(self, label, command):
        self._entries.append(
            MenuEntry(label=label, value=command))

    def add_cascade(self, label, menu):
        self._entries.append(
            MenuEntry(label=label, value=menu, cascade=True))

    @property
    def entries(self):
        res = []
        if self.parent:
            res.append(
                MenuEntry(**{'label': _(u'<go back>'), 'value': self.parent}))
        if self.root:
            res.append(
                MenuEntry(**{'label': _(u'<exit>'), 'value': None}))
        # idx = self.start_idx
        for e in self._entries:
            # label = u'{idx}: {label}'.format(idx=idx, label=e.label)
            # res.append(MenuEntry(**{u'label': label, u'value': e.value}))
            # idx += 1
            res.append(e)
        return res

    def __repr__(self):
        myself = "<i3menu.menu.Menu object '{title}'>".format(
            title=self.name)
        return myself


class I3Menu(Menu):
    def __init__(self, *args, **kwargs):
        super(I3Menu, self).__init__(*args, **kwargs)
        self.i3 = I3Connector()


class ActionsMenu(Menu):

    def __init__(self, *args, **kwargs):
        actions = []
        if 'actions' in kwargs:
            actions = kwargs.pop('actions')
        self._actions = actions
        super(ActionsMenu, self).__init__(*args, **kwargs)

    @property
    def entries(self):
        res = []
        for a in self._actions:
            entry = MenuEntry(**{'label': a, 'value': a})
            res.append(entry)
        return res


class WindowsMenu(I3Menu):

    @property
    def entries(self):
        wins = self.i3.get_windows()
        # if scratchpad:
        #     wins = self.conn.get_scratchpad_windows()
        wins = sorted(wins, key=lambda x: x.window_class)
        if self.filter_fnc:
            tmp = [e for e in filter(self.filter_fnc, wins)]
            wins = tmp
        entries = []
        for win in wins:
            params = {'window': win}
            label = LABEL_WINDOW.format(**params)
            entry = MenuEntry(**{'label': label, 'value': win})
            entries.append(entry)
        return entries


class WorkspacesMenu(I3Menu):

    @property
    def entries(self):
        workspaces = self.i3.get_workspaces()
        workspaces = sorted(workspaces, key=lambda x: x.name)
        if self.filter_fnc:
            workspaces = [e for e in filter(self.filter_fnc, workspaces)]
        entries = []
        for ws in workspaces:
            params = {}
            params = {'name': ws.name}
            params['current'] = ws.focused and ' (current)' or ''
            label = LABEL_WORKSPACE.format(**params)
            entry = MenuEntry(**{'label': label, 'value': ws})
            entries.append(entry)
        return entries


class OutputsMenu(I3Menu):

    @property
    def entries(self):
        outputs = self.i3.get_active_outputs()
        focused = self.i3.get_focused_output()
        outputs = sorted(outputs, key=lambda x: x.name)
        entries = []
        if self.filter_fnc:
            outputs = [e for e in filter(self.filter_fnc, outputs)]
        else:
            entries.extend(XRANDR_DIRECTIONS)
        for out in outputs:
            params = {'name': out.name}
            params['current'] = out.name == focused.name \
                and ' (current)' or ''
            label = LABEL_OUTPUT.format(**params)
            entry = MenuEntry(**{'label': label, 'value': out})
            entries.append(entry)
        return entries


def recursive_menu_traverse(menu, results=None):
    results = results or []
    if isinstance(menu, Menu):
        results.append(menu)
        for child in menu.entries:
            if isinstance(child, MenuEntry) and \
                    isinstance(child.value, Menu):
                results.extend(
                    recursive_menu_traverse(child.value, results))
    return list(set(results))


def menu_root(tree, root_name):
    menus_list = recursive_menu_traverse(tree)
    res = None
    for m in menus_list:
        if m.name == root_name:
            res = m
    if res:
        return res
    else:
        return tree


def menu_list(tree):
    menu_list = recursive_menu_traverse(tree)
    sorted_list = sorted(menu_list, key=lambda m: m.name)
    return [m.name for m in sorted_list]


def display_menu(menu_provider, menu, prompt=None, filter_fnc=None):
    entries = menu.entries
    if filter_fnc:
        entries = [e for e in filter(filter_fnc, entries)]
    if len(entries) == 1:
        logger.info('This menu has just one option, no need to diplay it')
        return entries[0]
    prompt = u'{appname} {prompt}'.format(
        appname=__name__,
        prompt=menu.prompt)
    encoded_prompt = '"%s": ' % prompt
    cmd_args = []
    if 'rofi' in menu_provider or 'dmenu' in menu_provider:
        cmd_args = ['-p', encoded_prompt]
    if 'rofi' in menu_provider:
        cmd_args = ['-dmenu'] + cmd_args
    encoded_args = safe_join(cmd_args, ' ')
    labels = []
    for i, e in enumerate(entries):
        icon = e.cascade and SUBMENU_SIGN or MENUENTRY_SIGN
        label = u'{idx}: {l}{icon}'.format(
            idx=i,
            l=e.label,
            icon=icon)
        labels.append(label)
    encoded_labels = safe_join(labels, '\n')
    cmd = 'echo "{options}" | {cmd} {cmd_args}'.format(
        cmd=menu_provider,
        cmd_args=encoded_args,
        options=encoded_labels,
    )
    logger.info('Display menu: ' + repr(cmd))
    proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    res = proc.stdout.read().decode('utf-8').strip('\n')
    res = res.strip(SUBMENU_SIGN).strip(MENUENTRY_SIGN).split(': ', 1)[-1]
    if len(entries) == 0:
        return res
    for e in entries:
        if e.label == res:
            return e


def mainloop(menu_provider, menu, filter_fnc=None):
    entry = display_menu(menu_provider, menu, filter_fnc=filter_fnc)
    if not entry:
        return None
    elif isinstance(entry, six.string_types):
        return entry
    elif isinstance(entry.value, Menu):
        newmenu = entry.value
        if not newmenu.root:
            newmenu.parent = menu
        return mainloop(menu_provider, newmenu)
    elif entry:
        return entry.value
    return None
