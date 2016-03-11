# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import six
import mock


class MockWindow(object):
    window_class = u'Mock'
    window_instance = u'mock'
    name = u'Mock'
    fullscreen_mode = 0
    current_border_width = 2
    urgent = False
    num = None
    border = u'normal'
    id = "11111111"
    orientation = u'none'
    layout = u'splith'
    percent = None
    mark = None
    window = "00000000"
    nodes = []
    type = u'con'
    focused = False
    floating_nodes = []

    def __init__(self, *args, **kwargs):
        for k, v in six.iteritems(*args):
            setattr(self, k, v)


class MockWorkspace(object):
    num = 1
    name = "MockWorkspace"
    visible = True
    focused = False
    rect = {"x": 0, "y": 20, "width": 1920, "height": 1060}
    output = "mockoutput"
    urgent = False

    def __init__(self, *args, **kwargs):
        for k, v in six.iteritems(*args):
            setattr(self, k, v)


class MockOutput(object):
    name = "MockOutput"
    active = True
    primary = True
    rect = {"x": 0, "y": 0, "width": 1920, "height": 1080}
    current_workspace = "MockWorkspace"

    def __init__(self, *args, **kwargs):
        for k, v in six.iteritems(*args):
            setattr(self, k, v)

MOCK_OUTPUT1 = MockWorkspace({'name': 'MockOutput1'})
MOCK_OUTPUT2 = MockWorkspace({'name': 'MockOutput2'})

MOCK_OUTPUTS_LIST = [MOCK_OUTPUT1, MOCK_OUTPUT2]

MOCK_WORKSPACE1 = MockWorkspace(
    {'name': 'MockWorkspace1', 'output': 'XYZ', 'focused': True})
MOCK_WORKSPACE2 = MockWorkspace(
    {'name': 'MockWorkspace2', 'output': 'XYZ'})
MOCK_WORKSPACE3 = MockWorkspace(
    {'name': 'MockWorkspace3', 'output': 'XYZ'})

MOCK_WORKSPACES_LIST = [MOCK_WORKSPACE1, MOCK_WORKSPACE2, MOCK_WORKSPACE3]


MOCK_WINDOW1 = MockWindow(
    {
        'window_instance': u'mockwindow1',
        'window_class': u'MockWindow',
        'name': u'MockWindow1',
        'focused': True,
    }
)
MOCK_WINDOW2 = MockWindow(
    {
        'window_instance': u'mockwindow2',
        'window_class': u'MockWindow',
        'name': u'MockWindow2',
    }
)
MOCK_WINDOW3 = MockWindow(
    {
        'window_instance': u'mockwindow3',
        'window_class': u'MockWindow',
        'name': u'MockWindow3'
    }
)
MOCK_WINDOWS_LIST = [MOCK_WINDOW1, MOCK_WINDOW2, MOCK_WINDOW3]

conn = mock.MagicMock()
conn.i3 = None
conn.get_windows.return_value = MOCK_WINDOWS_LIST
conn.get_workspaces.return_value = MOCK_WORKSPACES_LIST
conn.get_outputs.return_value = MOCK_OUTPUTS_LIST

MOCK_CONNECTOR = conn

MOCK_CONTEXT = mock.MagicMock()
MOCK_CONTEXT.i3.get_windows.return_value = MOCK_WINDOWS_LIST
MOCK_CONTEXT.i3.get_workspaces.return_value = MOCK_WORKSPACES_LIST
MOCK_CONTEXT.i3.get_active_outputs.return_value = MOCK_OUTPUTS_LIST
