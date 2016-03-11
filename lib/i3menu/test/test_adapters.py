# -*- coding: utf-8 -*-
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from zope.component import getGlobalSiteManager
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from i3menu.interfaces import IMenu

gsm = getGlobalSiteManager()

FAKE_CONTEXT = {}


class TestAdapters(unittest.TestCase):
    def test_menu_adapter(self):
        vocab = SimpleVocabulary([
            SimpleTerm('a', 'a', 'a'),
            SimpleTerm('b', 'b', 'b'),
        ])
        menu_adapter = IMenu(vocab)
        menu = menu_adapter(FAKE_CONTEXT)
        self.assertEqual(len(menu.entries), 2)
