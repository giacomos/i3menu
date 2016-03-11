# -*- coding: utf-8 -*-
from i3menu import _

SUBMENU_SIGN = u' ⇲'
MENUENTRY_SIGN = u''
PROMPT_PREFIX = u'(i3menu)'
DEFAULT_TITLE = _(u'Select')
LABEL_GENERIC = u'{idx}: {entry}'
# LABEL_WINDOW = u'{idx}: {window_class}\t{name}'
LABEL_WINDOW = u'{window.window_class}\t{window.name}'
LABEL_OUTPUT = u'{name}{current}'
LABEL_WORKSPACE = u'{name}{current}'

DEFAULTS = {
    'prompt_prefix': PROMPT_PREFIX,
    'prompt': DEFAULT_TITLE,
    'label_generic': LABEL_GENERIC,
    'label_window': LABEL_WINDOW,
    'label_output': LABEL_OUTPUT,
    'label_workspace': LABEL_WORKSPACE
}


class DummyOutput(object):
    name = None

    def __init__(self, name):
        self.name = name


XRANDR_DIRECTION_LEFT = DummyOutput('left')
XRANDR_DIRECTION_RIGHT = DummyOutput('right')
XRANDR_DIRECTION_UP = DummyOutput('up')
XRANDR_DIRECTION_DOWN = DummyOutput('down')

XRANDR_DIRECTIONS = [
    XRANDR_DIRECTION_LEFT,
    XRANDR_DIRECTION_RIGHT,
    XRANDR_DIRECTION_UP,
    XRANDR_DIRECTION_DOWN
]
