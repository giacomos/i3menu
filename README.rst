Introduction
============

**i3menu** provides a useful set of menus based on `Rofi
<https://davedavenport.github.io/rofi>`_ to interact with `i3wm
<http://i3wm.org>`_.

Installation
============
::

    $ sudo pip install i3menu

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
