# -*- coding: utf-8 -*-
import sys
import subprocess
from zope.component import getGlobalSiteManager
from zope.interface import implementer

from i3menu import logger
from i3menu.utils import safe_join
from i3menu.utils import safe_decode
from i3menu.config import SUBMENU_SIGN
from i3menu.config import MENUENTRY_SIGN
from i3menu.__about__ import __title__
from i3menu.interfaces import IMenuProvider
from i3menu.interfaces import IContextManager
from i3menu.interfaces import II3Connector

gsm = getGlobalSiteManager()


@implementer(IMenuProvider)
class MenuProvider(object):

    def __init__(self, cmd):
        self.mp = cmd

    def display_menu(self, menu, prompt=None, filter_fnc=None):
        entries = menu.entries
        if filter_fnc:
            entries = [e for e in filter(filter_fnc, entries)]
        prompt = u'({appname}) {prompt}'.format(
            appname=__title__,
            prompt=menu.prompt)
        encoded_prompt = '"%s": ' % prompt
        cmd_args = []
        if 'rofi' in self.mp or 'dmenu' in self.mp:
            cmd_args = ['-p', encoded_prompt]
        if 'rofi' in self.mp:
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
            cmd=self.mp,
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
            if safe_decode(e.label) == res:
                return e
        sys.exit()

rofimp = MenuProvider('rofi')
gsm.registerUtility(rofimp, IMenuProvider, 'rofi')


@implementer(IContextManager)
class Context(object):
    pass


gsm.registerUtility(Context())


@implementer(II3Connector)
class I3Connector(object):

    def __init__(self):
        try:
            import i3ipc
            self.i3 = i3ipc.Connection()
        except:
            self.i3 = None
            logger.error('No i3wm connection found. Are you using i3?')

    def get_tree(self):
        return self.i3 and self.i3.get_tree() or None

    def get_workspaces(self):
        return self.i3 and self.i3.get_workspaces() or []

    def get_outputs(self):
        return self.i3 and self.i3.get_outputs() or []

    def get_windows(self):
        tree = self.get_tree()
        return tree and tree.leaves() or []

    def get_focused_window(self):
        tree = self.get_tree()
        return tree and tree.find_focused() or None

    def get_scratchpad_windows(self):
        return self.i3 and self.i3.get_tree().scratchpad().leaves() or []

    def get_focused_workspace(self):
        win = self.get_focused_window()
        return win and win.workspace() or None

    def get_active_outputs(self):
        outputs = self.get_outputs()
        active_outputs = []
        if outputs:
            active_outputs = [o for o in filter(lambda o: o.active, outputs)]
        return active_outputs

    def get_focused_output(self):
        ws = self.get_focused_workspace()
        return ws and ws.parent.parent or None

    def get_unfocused_outputs(self):
        active_outputs = self.get_active_outputs()
        focused_output = self.get_focused_output()
        active_outputs.pop(active_outputs.index(focused_output))
        return active_outputs

    def get_bar_ids(self):
        return self.i3 and self.i3.get_bar_config_list()

    def command(self, cmd):
        res = self.i3 and self.i3.command(cmd) or None
        return res


def get_connector():
    return I3Connector()

gsm = getGlobalSiteManager()
gsm.registerUtility(get_connector())
