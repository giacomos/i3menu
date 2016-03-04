# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import mock
import unittest
from i3menu.connector import I3Connector
from . import MOCK_WINDOWS_LIST
from . import MOCK_OUTPUTS_LIST
from . import MOCK_OUTPUT1
from . import MOCK_WINDOW2

#
# @mock.patch.object(I3Connector, 'get_windows')
# def mock_get_windows(mock_method):
#     mock_method.return_value = MOCK_WINDOWS_LIST


# class TestConnector(unittest.TestCase):
#
#     @mock.patch.object(I3Connector, 'get_windows')
#     def test_get_windows(self, patch):
#         patch.return_value = MOCK_WINDOWS_LIST
#         conn = I3Connector()
#         self.assertEqual(conn.get_windows(), MOCK_WINDOWS_LIST)
#
#     @mock.patch.object(I3Connector, 'get_outputs')
#     def test_get_focused_window(self, patch):
#         patch.return_value = MOCK_OUTPUTS_LIST
#         conn = I3Connector()
#         self.assertEqual(conn.get_active_outputs(), MOCK_OUTPUT1)
