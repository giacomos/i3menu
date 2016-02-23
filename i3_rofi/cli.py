import argparse
from i3_rofi import I3Rofi


def run():
    i3rofi = I3Rofi()
    parser = argparse.ArgumentParser(
        description='Provides rofi menus to interact with i3')
    parser.add_argument(
        "-m", "--menu", dest="menu", required=True,
        choices=i3rofi.menus,
        help="Menu to display"
    )
    parser.add_argument(
        "-d", "--debug", action='store_true',
        help="Display debug infos"
    )
    args = parser.parse_args()
    i3rofi.run(args)
