# -*- coding: utf-8 -*-
import i3ipc


class I3Connector(object):

    @property
    def i3(self):
        try:
            return i3ipc.Connection()
        except:
            return None

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
        win = self.get_focused_window()
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

    def command(self, cmd, debug=False):
        res = self.i3.command(cmd)
        return res
