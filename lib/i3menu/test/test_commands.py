# -*- coding: utf-8 -*-
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from zope.interface import Interface
from zope.component import getGlobalSiteManager
from i3menu.fields import Choice

from i3menu.test import BaseTestCase
from i3menu.factories import FocusedWindowFactory
from i3menu.commands import AbstractCmd, Floating
from i3menu.test import MOCK_WINDOW1

gsm = getGlobalSiteManager()


class IMockCommand(Interface):
    mock1 = Choice(title=u'mock1', values=['a', 'b'])


class MockCommand(AbstractCmd):
    schema = IMockCommand


class TestCommands(BaseTestCase):

    def test_abstract_cmd_get_defaults(self):
        cmd = AbstractCmd(self.context)
        fields = [
            ('mock1', Choice(title=u'mock1', values=['a', 'b'], default='a'))
        ]
        defaults = cmd.get_defaults(fields)
        self.assertEqual(defaults.get('mock1'), 'a')
        fields = [(
            'mock_window',
            Choice(
                title=u"Window",
                required=True,
                vocabulary="windows_vocabulary",
                defaultFactory=FocusedWindowFactory()
            )
        )]
        defaults = cmd.get_defaults(fields)
        self.assertEqual(defaults.get('mock_window'), MOCK_WINDOW1)

    def test_abstract_cmd_validate(self):
        cmd = MockCommand(self.context)
        self.assertEqual(len(cmd.validate()), 1)
        cmd.form.mock1 = 'a'
        self.assertEqual(cmd.validate(), {})

    def test_get_fields(self):
        cmd = Floating(self.context)
        self.assertEqual(len(cmd.form.fields()), 2)
