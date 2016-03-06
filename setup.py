from __future__ import absolute_import, division, print_function
import sys
from os import path
from codecs import open

try:
    from setuptools import setup
except ImportError:
    print("i3menu needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

sys.path.insert(0, path.abspath('lib'))
from i3menu.__about__ import (
    __author__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'docs', 'HISTORY.rst'), encoding='utf-8') as f:
    long_description = '\n'.join((long_description, f.read()))

setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Operating System :: Unix",
        "Topic :: Desktop Environment :: Window Managers",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='i3 i3wm rofi dmenu',
    author=__author__,
    author_email=__email__,
    url=__uri__,
    license=__license__,
    package_dir={'': 'lib'},
    packages=['i3menu'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools', 'i3ipc', 'argparse', 'six'],
    scripts=['bin/i3menu'],
    entry_points={},
)
