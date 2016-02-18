import argparse
from i3_rofi import I3Rofi


def run():
    conn = I3Rofi()
    menus = {
        'go_to_workspace': conn.go_to_workspace,
        'move_window_to_workspace': conn.move_window_to_workspace,
        'move_window_to_this_workspace': conn.move_window_to_this_workspace,
        'move_workspace_to_output': conn.move_workspace_to_output,
        'rename_workspace': conn.rename_workspace,
        'window_actions': conn.window_actions,
        'workspace_actions': conn.workspace_actions
    }
    parser = argparse.ArgumentParser(
        description='Provides rofi menus to interact with i3')
    parser.add_argument(
        "-m", "--menu", dest="menu",
        help="Menu to display. Available menus: %s" % ', '.join(menus.keys())
    )
    args = parser.parse_args()
    if args.menu in menus:
        menu = menus[args.menu]
        menu()
