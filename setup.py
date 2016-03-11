from __future__ import absolute_import, division, print_function
import sys
from setuptools import setup
from setuptools.command.sdist import sdist
from codecs import open
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import abspath
from os.path import splitext

# sys.path.insert(0, abspath('lib'))
# from i3menu.__about__ import (
#     __author__, __email__, __license__, __summary__, __title__,
#     __uri__, __version__
# )

here = abspath(dirname(__file__))

with open(join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
with open(join(here, 'docs', 'HISTORY.rst'), encoding='utf-8') as f:
    long_description = '\n'.join((long_description, f.read()))

# needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
# pytest_runner = ['pytest-runner'] if needs_pytest else []
# pytest_runner = ['pytest-runner']
about = {}
with open(join(here, 'lib', 'i3menu', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)


class CompileLocales(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""

    def run(self):
        self.run_command('compile_catalog')
        # sdist is an old style class so super cannot be used.
        sdist.run(self)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
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
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__uri__'],
    license=about['__license__'],
    packages=['i3menu'],
    package_dir={'': 'lib'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'zope.interface',
        'zope.schema',
        'zope.component',
        'i3ipc',
        'six'
    ],
    setup_requires=['Babel'],
    tests_require=['mock', 'unittest2'],
    cmdclass={'sdist': CompileLocales},
    scripts=['bin/i3menu'],
    entry_points={},
)
