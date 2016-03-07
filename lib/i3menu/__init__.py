# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import sys
from i3menu import i18n

import logging

from .__about__ import (
    __author__, __copyright__, __email__, __license__, __longlicense__,
    __summary__, __title__, __uri__, __version__
)

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__longlicense__", "__copyright__",
]

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

_ = i18n.language.gettext

# https://github.com/jaraco/setuptools/blob/master/pkg_resources/_vendor/six.py
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
