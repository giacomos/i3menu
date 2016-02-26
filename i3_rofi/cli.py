import argparse
import sys
import errno
from i3_rofi import I3Rofi
from . import commands
from . import menus
from .utils import which


def run():
    if not which('rofi'):
        sys.exit(errno.EINVAL)
    i3rofi = I3Rofi()
    all_commands = commands.all_commands()
    all_menus = menus.all_menus()
    all_choices = all_commands.keys() + all_menus.keys()

    parser = argparse.ArgumentParser(
        description='Provides rofi menus to interact with i3')
    parser.add_argument(
        "-m", "--menu", dest="menu", required=True,
        choices=all_choices,
        help="Menu to display"
    )
    parser.add_argument(
        "-d", "--debug", action='store_true',
        help="Display debug infos"
    )
    args = parser.parse_args()
    opt = args.menu
    if opt in all_menus.keys():
        Menu = all_menus[opt]
        menu = Menu()
        menu()
    elif opt in all_commands.keys():
        Command = all_commands[opt]
        cmd = Command()
        cmd()
    else:
        sys.exit(errno.EINVAL)
