# -*- coding: utf-8 -*-
from i3menu import _

PROMPT_PREFIX = u'(i3menu)'
DEFAULT_TITLE = _(u'Select:')
LABEL_GENERIC = u'{idx}: {entry}'
# LABEL_WINDOW = u'{idx}: {window_class}\t{name}'
LABEL_WINDOW = u'{idx}: {window.window_class}\t{window.name}'
LABEL_OUTPUT = u'{idx}: {name}{current}'
LABEL_WORKSPACE = u'{name}{current}'

DEFAULTS = {
    'prompt_prefix': PROMPT_PREFIX,
    'prompt': DEFAULT_TITLE,
    'label_generic': LABEL_GENERIC,
    'label_window': LABEL_WINDOW,
    'label_output': LABEL_OUTPUT,
    'label_workspace': LABEL_WORKSPACE
}

XRANDR_DIRECTION_LEFT = {'name': u'left'}
XRANDR_DIRECTION_RIGHT = {'name': u'right'}
XRANDR_DIRECTION_UP = {'name': u'up'}
XRANDR_DIRECTION_DOWN = {'name': u'down'}

XRANDR_DIRECTIONS = [
    XRANDR_DIRECTION_LEFT,
    XRANDR_DIRECTION_RIGHT,
    XRANDR_DIRECTION_UP,
    XRANDR_DIRECTION_DOWN
]
