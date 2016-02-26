import argparse
import sys
import errno
from i3menu import commands
from i3menu import menus
from i3menu.utils import which


def run():
    if not which('rofi'):
        sys.exit(errno.EINVAL)
    all_commands = commands.all_commands()
    all_actions = set()
    for k, cmd in all_commands.iteritems():
        all_actions |= set(cmd._actions)
    all_menus = menus.all_menus()

    parser = argparse.ArgumentParser(
        description='Provides rofi menus to interact with i3',
        prog='i3menu', version='2.0')
    parser.add_argument(
        "-d", "--debug", action='store_true',
        help="Debug, print the i3 command before executing it"
    )
    # parser.add_argument(
    #     "action",
    #     choices=all_actions,
    #     help=""
    # )

    mutgrp = parser.add_mutually_exclusive_group()
    mutgrp.add_argument(
        "-m", "--menu", dest="menu", help="Menu to display", metavar='<menu>',
        choices=all_menus.keys()
    )
    mutgrp.add_argument(
        "-c", "--command", dest="command", help="Command to execute", metavar='<command>',
        choices=all_commands.keys()
    )
    for k, cmd in all_commands.iteritems():
        mutgrp.add_argument(
            '--' + k, help=cmd._description,
            dest='cmd', action='append_const', const=cmd)
    args = parser.parse_args()
    res = {}
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if args.cmd:
        Command = args.cmd[0]
        if args.action in Command._actions:
            cmd = Command(args.action)
        else:
            cmd = Command()
        res = cmd(debug=args.debug)
    elif args.menu:
        Menu = all_menus.get(args.menu)
        if not Menu:
            sys.exit(errno.EINVAL)
        menu = Menu()
        res = menu(debug=args.debug)
    elif args.command:
        Command = all_commands.get(args.command)
        if not Command:
            sys.exit(errno.EINVAL)
        cmd = Command()
        res = cmd(debug=args.debug)
    if not res:
        sys.exit(errno.EINVAL)
    if res.get('success'):
        sys.exit()
    else:
        sys.exit('Error: ' + res.get('error'))

if __name__ == '__main__':
    run()
