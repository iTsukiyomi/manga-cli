import argparse
from manga_cli import __version__
from manga_cli.tui import run_tui


def build_parser():
    parser = argparse.ArgumentParser(
        prog="manga-cli",
        description="A terminal manga reader, like ani-cli but for manga",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  manga-cli                      Open interactive search
  manga-cli -s "one piece"       Search directly for 'one piece'
  manga-cli -c                   Continue last read manga
  manga-cli --version            Print version
""",
    )

    parser.add_argument(
        "-s", "--search",
        metavar="QUERY",
        type=str,
        help="Search for a manga by name and open the chapter list.",
    )

    parser.add_argument(
        "-c", "--continue",
        dest="continue_reading",
        action="store_true",
        help="Continue reading the last manga from where you left off",
    )

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Print version and exit."
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"manga-cli v{__version__}")
    elif args.continue_reading:
        print(f"[continue] not yet implemented")
    elif args.search:
        run_tui(args.search)
    else:
        run_tui()

    

if __name__ == "__main__":
    main()