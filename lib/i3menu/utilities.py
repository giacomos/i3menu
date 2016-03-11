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
