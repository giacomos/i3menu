# -*- coding: utf-8 -*-
import i3ipc
from i3menu.config import DEFAULTS
from i3menu import logger


class I3Connector(object):

    def __init__(self, config=None):
        if not config:
            config = DEFAULTS
        self.config = config
        try:
            self.i3 = i3ipc.Connection()
        except:
            self.i3 = None

    def get_workspaces(self):
        return self.i3.get_workspaces()

    def get_outputs(self):
        return self.i3.get_outputs()

    def get_windows(self):
        return self.i3.get_tree().leaves()

    def get_focused_window(self):
        return self.i3.get_tree().find_focused()

    def get_scratchpad_windows(self):
        return self.i3.get_tree().scratchpad().leaves()

    def get_focused_workspace(self):
        win = self.get_window()
        return win.workspace()

    def get_active_outputs(self):
        outputs = self.i3.get_outputs()
        return [o for o in filter(lambda o: o.active, outputs)]

    def get_focused_output(self):
        ws = self.get_focused_workspace()
        out = ws.parent.parent
        return out

    def get_unfocused_outputs(self):
        active_outputs = self.get_active_outputs()
        focused_output = self.get_focused_output()
        active_outputs.pop(active_outputs.index(focused_output))
        return active_outputs

    def get_bar_ids(self):
        return self.i3.get_bar_config_list()

    def command(self, cmd):
        if self.config.get('debug'):
            logger.info(cmd)
        res = self.i3.command(cmd)
        return res
