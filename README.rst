Introduction
============

**i3menu** provides a useful set of menus based on `Rofi
<https://davedavenport.github.io/rofi>`_  and `dmenu
<http://tools.suckless.org/dmenu/>`_ to interact with `i3wm
<http://i3wm.org>`_.

Requirements
============

`i3menu` requires either `Rofi
<https://davedavenport.github.io/rofi>`_  or `dmenu
<http://tools.suckless.org/dmenu/>`_ to work.

dmenu is pretty easy to install::

    sudo apt-get install suckless-tools

But `Rofi` is way much nicer. To install it follow its the `installation guide
<https://davedavenport.github.io/rofi/p08-INSTALL.html>`_.

Installation
============
`i3menu` can be installed with ::
    
    $ pip install i3menu

This will add a script in your local bin path, `~/.local/bin`. If your $PATH
is set up correctly, now you should be able to run i3menu::

    $ i3menu -h

If the command is not found, please check your $PATH to be sure to have your local bin
path::

    $ PATH=$PATH:~/.local/bin

Usage
=====
You can use i3menu directly from the command line::

    $ i3menu --help

or::

    $ i3menu window_actions

You can add i3menu to your i3 config. For example::

    bindsym $mod+w exec --no-startup-id i3menu goto_workspace

or::

    bindsym $mod+w exec --no-startup-id i3menu -m go_to_workspace

Credits
=======

* partially inspired by `quickswitch-i3 <https://pypi.python.org/pypi/quickswitch-i3>`_


License
========

**Disclaimer: i3menu is a third party script and in no way affiliated
with the i3 project, the dmenu project or the rofi project.**
