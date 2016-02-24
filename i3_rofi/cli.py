import argparse
from i3_rofi import I3Rofi


def run():
    parser = argparse.ArgumentParser(
        description='Provides rofi menus to interact with i3')
    parser.add_argument(
        "-m", "--menu", dest="menu", required=True,
        choices=I3Rofi.menus,
        help="Menu to display"
    )
    parser.add_argument(
        "-d", "--debug", action='store_true',
        help="Display debug infos"
    )
    args = parser.parse_args()
    i3rofi = I3Rofi(menu=args.menu, debug=args.debug)
    i3rofi()
