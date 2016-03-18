# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import sys
import gettext
import logging
from os import path

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

here = path.abspath(path.dirname(__file__))
localedir = path.join(here, 'locale')
translate = gettext.translation(__title__, localedir, fallback=True)
_ = translate.gettext

# https://github.com/jaraco/setuptools/blob/master/pkg_resources/_vendor/six.py
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)

from i3menu import patches  # noqa
from i3menu import factories  # noqa
from i3menu import interfaces  # noqa
from i3menu import utilities  # noqa
from i3menu import adapters  # noqa
from i3menu import commands  # noqa
