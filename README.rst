Introduction
============

**i3menu** provides a useful set of menus based on `Rofi
<https://davedavenport.github.io/rofi>`_  and `dmenu
<http://tools.suckless.org/dmenu/>`_ to interact with `i3wm
<http://i3wm.org>`_.

Installation
============
`i3menu` can be installed in a `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ ::
    
    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install i3menu
    $ i3menu -h

If you use a virtualenv, remember to always source you virtual env in order
to have the `i3menu` command in your $PATH.

If you are comfortable with installing it system-wide, it can also be
installe using::

    $ sudo pip install i3menu
    $ i3menu -h

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
