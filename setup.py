import os
import codecs
from setuptools import setup
from setuptools import find_packages

version = '1.0'
install_requires = [
    'setuptools',
    'i3-py'
]

console_scripts = [
    'i3_go_to_workspace = i3_rofi:go_to_workspace',
    'i3_move_window_to_workspace = i3_rofi:move_window_to_workspace',
    'i3_move_window_to_this_workspace = i3_rofi:move_window_to_this_workspace',
    'i3_move_workspace_to_output = i3_rofi:move_workspace_to_output',
    'i3_rename_workspace = i3_rofi:rename_workspace',
    'i3_window_actions = i3_rofi:window_actions',
    'i3_workspace_actions = i3_rofi:workspace_actions',
]


def read(*rnames):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), *rnames), 'r', 'utf-8').read()


setup(
    name='i3-rofi',
    version=version,
    description="",
    long_description=read('README.rst') + '\n' + read('HISTORY.rst'),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='i3 i3wm rofi',
    author='Giacomo Spettoli',
    author_email='giacomo.spettoli@gmail.com',
    url='https://github.com/giacomos/i3-rofi',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={'console_scripts': console_scripts}
)
