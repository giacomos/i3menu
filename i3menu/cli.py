import argparse
import sys
import errno
from i3menu import commands
from i3menu import menus
from i3menu.utils import which
from i3menu.utils import iteritems


def run():
    if not which('rofi'):
        sys.exit(errno.EINVAL)
    all_commands = commands.all_commands()
    all_menus = menus.all_menus()
    all_actions = set()
    for k, cmd in iteritems(all_commands):
        all_actions |= set(cmd._actions)
    options = menus.all_menus().keys() + commands.all_commands().keys()

    parser = argparse.ArgumentParser(
        description='Provides rofi menus to interact with i3',
        prog='i3menu', version='2.0')
    parser.add_argument(
        "-d", "--debug", action='store_true',
        help="Debug, print the i3 command before executing it"
    )
    parser.add_argument(
        "--menu-provider", dest='menu_provider',
        choices=['dmenu', 'rofi'],
        help="Force the use of a menu provider"
    )
    parser.add_argument(
        "--action", dest='action', metavar='<action>',
        choices=all_actions,
        help="""Command action. Depending on the command not all action
may be available. Allowed values are: """ + ", ".join(all_actions),
    )
    parser.add_argument(
        "menu",
        choices=options,
        help="Menu to be executed. Allowed values are: " + ", ".join(options),
        metavar='<menu>')
    args = parser.parse_args()
    res = []
    context = {}
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if args.debug:
        context['debug'] = True
    if args.menu_provider:
        context['menu_provider'] = args.menu_provider
    if args.action:
        context['action'] = args.action

    menu = args.menu
    if menu in all_commands:
        Command = all_commands[menu]
        cmd = Command(context=context)
    elif menu in all_menus:
        Menu = all_menus[menu]
        cmd = Menu(context=context)
    res = cmd()
    if not res:
        sys.exit(errno.EINVAL)
    res = res[0]
    if res.get('success'):
        sys.exit()
    else:
        sys.exit('Error: ' + res.get('error'))

if __name__ == '__main__':
    run()
