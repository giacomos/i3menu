import os
import codecs
from setuptools import setup
from setuptools import find_packages

version = '2.0.1'
install_requires = [
    'setuptools',
    'i3ipc',
    'argparse',
]

console_scripts = [
    'i3menu = i3menu.cli:run',
]


def read(*rnames):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), *rnames), 'r', 'utf-8').read()


setup(
    name='i3menu',
    version=version,
    description="a set of menus based on Rofi or dmenu to interact with i3wm",
    long_description=read('README.rst') + '\n' + read('docs/HISTORY.rst'),
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
    author='Giacomo Spettoli',
    author_email='giacomo.spettoli@gmail.com',
    url='https://github.com/giacomos/i3menu',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={'console_scripts': console_scripts}
)
