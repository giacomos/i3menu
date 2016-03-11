# -*- coding: utf-8 -*-
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from zope.component import getGlobalSiteManager

from i3menu.test import BaseTestCase
from i3menu.test import MOCK_WINDOWS_LIST
from zope.component import getUtility
from i3menu.utilities import II3Connector

gsm = getGlobalSiteManager()


class TestConnector(BaseTestCase):

    def test_connector_get_windows(self):
        conn = getUtility(II3Connector)
        wins = conn.get_windows()
        self.assertEqual(len(wins), len(MOCK_WINDOWS_LIST))
