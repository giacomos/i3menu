# -*- coding: utf-8 -*-
from i3menu import _
from i3menu.connector import I3Connector
from i3menu.config import LABEL_WINDOW
from i3menu.config import LABEL_WORKSPACE
from i3menu.config import LABEL_OUTPUT


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
    prompt = u'Menu:'
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


class WindowsMenu(Menu):

    def __init__(self, *args, **kwargs):
        super(WindowsMenu, self).__init__(*args, **kwargs)
        self.i3 = I3Connector()

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


class WorkspacesMenu(Menu):

    def __init__(self, *args, **kwargs):
        super(WorkspacesMenu, self).__init__(*args, **kwargs)
        self.i3 = I3Connector()

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


class OutputsMenu(Menu):

    def __init__(self, *args, **kwargs):
        super(OutputsMenu, self).__init__(*args, **kwargs)
        self.i3 = I3Connector()

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
