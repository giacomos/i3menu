# -*- coding: utf-8 -*-
from i3menu.commands.base import AbstractCmd


class CmdShmlog(AbstractCmd):
    """ http://i3wm.org/docs/userguide.html#shmlog
    """

    _name = 'shmlog'
    # TODO: add the possibility to specify the shared memory size
    _actions = ['on', 'off', 'toggle']

    def cmd(self):
        action = self.get_action()
        return 'shmlog {action}'.format(action=action)
