"""Clean up old files."""

from argparse import ArgumentParser, Namespace

from ddbfiles.files import FILES

__all__ = ['main']


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-k', '--keep', type=int, default=3,
        help='amount of newest files to keep'
    )
    return parser.parse_args()


def main() -> None:
    """Run the cleanup script."""

    args = get_args()

    for file in FILES.values():
        for _, path in sorted(file.versions)[:-args.keep]:
            path.unlink()
