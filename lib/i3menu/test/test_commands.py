# -*- coding: utf-8 -*-
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest

from zope.component import getGlobalSiteManager
from zope.schema import Choice

from i3menu.vocabs import init_vocabs
from i3menu.factories import FocusedWindowFactory
from i3menu.commands import AbstractCmd, Floating
from i3menu.test import MOCK_CONTEXT, MOCK_WINDOW1

gsm = getGlobalSiteManager()


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.context = MOCK_CONTEXT
        init_vocabs(self.context)

    def test_abstract_cmd_get_defaults(self):
        cmd = AbstractCmd(self.context)
        params = [
            ('mock1', Choice(title=u'mock1', values=['a', 'b'], default='a'))
        ]
        cmd.params = params
        defaults = cmd.get_defaults()
        self.assertEqual(defaults.get('mock1'), 'a')
        params = [(
            'mock_window',
            Choice(
                title=u"Window",
                required=True,
                vocabulary="windows_vocabulary",
                defaultFactory=FocusedWindowFactory()
            )
        )]
        cmd.params = params
        defaults = cmd.get_defaults()
        self.assertEqual(defaults.get('mock_window'), MOCK_WINDOW1)

    def test_abstract_cmd_validate_data(self):
        cmd = AbstractCmd(self.context)
        params = [
            ('mock1', Choice(title=u'mock1', values=['a', 'b']))
        ]
        cmd.params = params
        self.assertFalse(cmd.validate_data())
        cmd.data = {'mock1': 'a'}
        self.assertTrue(cmd.validate_data())

    def test_get_params(self):
        cmd = Floating(self.context)
        self.assertEqual(len(cmd.params), 2)
