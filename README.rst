======
i3menu
======

.. list-table::
    :stub-columns: 1

    * - tests
      - |travis| |coveralls| |codecov|
    * - package
      - |version| |downloads| |wheel| |license| |status|

.. |travis| image:: https://img.shields.io/travis/giacomos/i3menu/master.svg?style=flat&label=travis
    :target: https://travis-ci.org/giacomos/i3menu
    :alt: TravisCI - i3menu

.. |coveralls| image:: https://img.shields.io/coveralls/giacomos/i3menu/master.svg?style=flat&label=coveralls
    :alt: coverage status
    :target: https://coveralls.io/github/giacomos/i3menu?branch=master

.. |codecov| image:: https://img.shields.io/codecov/c/github/giacomos/i3menu/master.svg?style=flat&label=codecov
    :alt: coverage status
    :target: https://codecov.io/github/giacomos/i3menu

.. |version| image:: https://img.shields.io/pypi/v/i3menu.svg
   :target: https://pypi.python.org/pypi/i3menu

.. |downloads| image:: https://img.shields.io/pypi/dm/i3menu.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/i3menu

.. |wheel| image:: https://img.shields.io/pypi/wheel/i3menu.svg
    :target: https://pypi.python.org/pypi/i3menu

.. |license| image:: https://img.shields.io/pypi/l/i3menu.svg
    :target: https://pypi.python.org/pypi/i3menu

.. |status| image:: https://img.shields.io/pypi/status/i3menu.svg
    :target: https://pypi.python.org/pypi/i3menu

Introduction
============

**i3menu** provides a useful set of menus based on `Rofi
<https://davedavenport.github.io/rofi>`_  and `dmenu
<http://tools.suckless.org/dmenu/>`_ that will help you manage you `i3wm
<http://i3wm.org>`_.

Requirements
============

`i3menu` requires either `Rofi
<https://davedavenport.github.io/rofi>`_  or `dmenu
<http://tools.suckless.org/dmenu/>`_ to work.

dmenu is pretty easy to install::

    sudo apt-get install suckless-tools

But `Rofi` is way much nicer. To install it follow its `installation guide
<https://davedavenport.github.io/rofi/p08-INSTALL.html>`_.

Installation
============
`i3menu` can be installed directly from `pypi
<https://pypi.python.org/pypi/i3menu>`_ like this::
    
    $ pip install i3menu

Or from source code like this::

    $ git clone https://github.com/giacomos/i3menu.git
    $ cd i3menu
    $ make install

Whatever installation method you choosed, you will end up having a script in your local bin path, `~/.local/bin`. If your $PATH
is set up correctly, now you should be able to run i3menu::

    $ i3menu -h

If the command is not found, please check your $PATH to be sure to have your local bin
path::

    $ PATH=$PATH:~/.local/bin

To make this change permanent, you can add to your `.profile` file this::

    if [ -d "$HOME/.local/bin" ] ; then
        PATH="$PATH:$HOME/.local/bin"
    fi

This change will be permanent at your next login.

Usage
=====
For a complete list of the command line parameters you can check the help::

    $ i3menu --help

Any available menu can be run like this::

    $ i3menu window_actions

I3WM config
================

You can add i3menu to your i3 config. For example::

    bindsym $mod+w exec --no-startup-id i3menu goto_workspace

or::

    bindsym $mod+w exec --no-startup-id i3menu -m go_to_workspace

For a more complete set of examples, please take a look at my `i3wm config
<https://github.com/giacomos/i3wm-config>`_

Credits
=======

* partially inspired by `quickswitch-i3 <https://pypi.python.org/pypi/quickswitch-i3>`_


License
========

**Disclaimer: i3menu is a third party script and in no way affiliated
with the i3 project, the dmenu project or the rofi project.**
