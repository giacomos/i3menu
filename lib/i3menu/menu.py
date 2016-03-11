# -*- coding: utf-8 -*-
from i3menu import _


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
        newentry = MenuEntry(label=label, value=command)
        self._entries.append(newentry)
        return newentry

    def add_cascade(self, label, menu):
        newentry = MenuEntry(label=label, value=menu, cascade=True)
        self._entries.append(newentry)
        return newentry

    @property
    def entries(self):
        res = []
        if self.parent and not self.root:
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
