# -*- coding: utf-8 -*-
from i3menu import _

PROMPT_PREFIX = '(i3menu)'
DEFAULT_TITLE = _('Select:')
LABEL_GENERIC = '{idx}: {entry}'
LABEL_WINDOW = '{idx}: {window_class}\t{name}'
LABEL_OUTPUT = '{idx}: {name}{current}'
LABEL_WORKSPACE = '{name}{current}'

DEFAULTS = {
    'prompt_prefix': PROMPT_PREFIX,
    'prompt': DEFAULT_TITLE,
    'label_generic': LABEL_GENERIC,
    'label_window': LABEL_WINDOW,
    'label_output': LABEL_OUTPUT,
    'label_workspace': LABEL_WORKSPACE
}
