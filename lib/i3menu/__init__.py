# -*- coding: utf-8 -*-
from i3menu import i18n

import logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

_ = i18n.language.gettext

__version__ = '3.0'
__author__ = 'Giacomo Spettoli'
