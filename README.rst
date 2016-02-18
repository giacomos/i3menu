Introduction
============

**i3-rofi** provides a useful set of menus based on
`Rofi<https://davedavenport.github.io/rofi`_ to interact with i3.

Installation
-------------

    $ sudo pip install i3-rofi

This will automatically create a set of console scripts that can be used
in your i3 config. For example::

    bindsym $mod+w exec --no-startup-id i3_window_actions


The complete list of scripts includes:

* i3_go_to_workspace
* i3_move_window_to_workspace
* i3_move_window_to_this_workspace
* i3_move_workspace_to_output
* i3_rename_workspace
* i3_window_actions
* i3_workspace_actions
