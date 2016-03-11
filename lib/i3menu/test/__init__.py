# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import mock
import unittest
from zope.component import getUtility
from i3menu.utilities import II3Connector
from i3menu.vocabs import init_vocabs

# {
#     u'visible': True,
#     u'urgent': False,
#     u'rect': {u'x': 0, u'y': 20, u'width': 1920, u'height': 1060},
#     u'output': u'eDP1',
#     u'name': u'WORKSPACE 2',
#     u'focused': False,
#     u'num': 2
# }

MOCK_WORKSPACE1 = mock.MagicMock()
MOCK_WORKSPACE2 = mock.MagicMock()
MOCK_WORKSPACE3 = mock.MagicMock()

MOCK_WORKSPACE1.name = u'MockWorkspace1'
MOCK_WORKSPACE2.name = u'MockWorkspace2'
MOCK_WORKSPACE3.name = u'MockWorkspace3'

MOCK_WORKSPACE1.output = u'Output1'
MOCK_WORKSPACE2.output = u'Output2'
MOCK_WORKSPACE3.output = u'Output2'

MOCK_WORKSPACES_LIST = [MOCK_WORKSPACE1, MOCK_WORKSPACE2, MOCK_WORKSPACE3]


# {
#     'rect': <i3ipc.Rect object at 0x7f976a944e90>
#     'window_instance': u'XYZ'
#     'orientation': u'none'
#     'layout': u'splith'
#     'type': u'con'
#     'mark': None
#     'window': 10485908
#     'nodes': []
#     'focused': False
#     'border': u'normal'
#     'floating_nodes': []
#     'name': u'XYZ'
#     'parent': <i3ipc.Con object at 0x7f976a944d50>
#     'current_border_width': 2
#     '_conn': <i3ipc.Connection object at 0x7f976b228690>
#     'urgent': False
#     'id': 31860240
#     'window_class': u'XYZ'
#     'percent': 1.0
#     'num': None
#     'props': <i3ipc._PropsObject object at 0x7f976a944e50>
#     'fullscreen_mode': 0
# }

MOCK_WINDOW1 = mock.MagicMock()
MOCK_WINDOW2 = mock.MagicMock()
MOCK_WINDOW3 = mock.MagicMock()

MOCK_WINDOW1.window_instance = u'mockwindow1'
MOCK_WINDOW2.window_instance = u'mockwindow2'
MOCK_WINDOW3.window_instance = u'mockwindow3'

MOCK_WINDOW1.workspace.return_value = MOCK_WORKSPACE1
MOCK_WINDOW2.workspace.return_value = MOCK_WORKSPACE2
MOCK_WINDOW3.workspace.return_value = MOCK_WORKSPACE2

MOCK_WINDOW1.window_class = u'MockWindow'
MOCK_WINDOW2.window_class = u'MockWindow'
MOCK_WINDOW3.window_class = u'MockWindow'

MOCK_WINDOW1.name = u'MockWindow1'
MOCK_WINDOW2.name = u'MockWindow2'
MOCK_WINDOW3.name = u'MockWindow3'

MOCK_WINDOW1.focused = True

MOCK_WINDOWS_LIST = [MOCK_WINDOW1, MOCK_WINDOW2, MOCK_WINDOW3]

# {
#     u'primary': False,
#     u'current_workspace': u'WORKSPACE1',
#     u'name': u'eDP1',
#     u'rect': {u'x': 0, u'y': 0, u'width': 1920, u'height': 1080},
#     u'active': True
# }
MOCK_OUTPUT1 = mock.MagicMock()
MOCK_OUTPUT2 = mock.MagicMock()
MOCK_OUTPUT3 = mock.MagicMock()

MOCK_OUTPUT1.name = u'MockOutput1'
MOCK_OUTPUT2.name = u'MockOutput2'
MOCK_OUTPUT3.name = u'MockOutput3'

MOCK_OUTPUT1.active = True
MOCK_OUTPUT2.active = True
MOCK_OUTPUT3.active = False

MOCK_OUTPUTS_LIST = [MOCK_OUTPUT1, MOCK_OUTPUT2, MOCK_OUTPUT3]

MOCK_CONTEXT = mock.MagicMock()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.context = MOCK_CONTEXT

        conn_ut = getUtility(II3Connector)

        patch_i3 = mock.patch.object(conn_ut, 'i3')
        self.patch_i3 = patch_i3.start()
        self.patch_i3.return_value = None

        mock_tree = mock.MagicMock()
        mock_tree.leaves.return_value = MOCK_WINDOWS_LIST
        mock_tree.find_focused.return_value = MOCK_WINDOW1

        patch_tree = mock.patch.object(conn_ut, 'get_tree')
        self.patch_tree = patch_tree.start()
        self.patch_tree.return_value = mock_tree

        patch_workspaces = mock.patch.object(conn_ut, 'get_workspaces')
        self.patch_workspaces = patch_workspaces.start()
        self.patch_workspaces.return_value = MOCK_WORKSPACES_LIST

        patch_outputs = mock.patch.object(conn_ut, 'get_outputs')
        self.patch_outputs = patch_outputs.start()
        self.patch_outputs.return_value = MOCK_OUTPUTS_LIST

        init_vocabs(self.context)

    def tearDown(self):
        mock.patch.stopall()
