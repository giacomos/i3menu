import os
import sys
import codecs

sys.path.insert(0, os.path.abspath('lib'))
from i3menu import __version__, __author__

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    print("i3menu needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)


def read(*rnames):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), *rnames), 'r', 'utf-8').read()


setup(
    name='i3menu',
    version=__version__,
    description="a set of menus based on Rofi or dmenu to interact with i3wm",
    long_description='\n\n'.join((
        read('README.rst'),
        read('docs/HISTORY.rst')
    )),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Topic :: Desktop Environment :: Window Managers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    keywords='i3 i3wm rofi dmenu',
    author=__author__,
    author_email='giacomo.spettoli@gmail.com',
    url='https://github.com/giacomos/i3menu',
    license='GPLv3',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'i3ipc',
        'argparse',
    ],
    scripts=[
        'bin/i3menu'
    ],
    entry_points="""
          # -*- Entry points: -*-
        """,
)
