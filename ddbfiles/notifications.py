"""Notifications about file updates."""

from argparse import ArgumentParser, Namespace
from functools import partial
from pathlib import Path
from re import match
from typing import Iterable

from configlib import load_config
from emaillib import EMail, Mailer
from his import Account, stakeholders

from ddbfiles.files import DDB_ISO_REGEX


__all__ = ["notify"]


TEMPLATE_FILE = Path("/usr/local/etc/ddbfiles.email.template")


def get_template() -> str:
    """Return the email body template."""

    with TEMPLATE_FILE.open("r", encoding="utf-8") as file:
        return file.read()


def notify(accounts: Iterable[Account], filename: str) -> None:
    """Notify the given accounts."""

    get_mailer().send(
        map(
            partial(generate_email, filename=filename),
            map(lambda account: account.email, accounts),
        )
    )


def generate_email(recipient: str, filename: str) -> EMail:
    """Yield emails for the respective recipients."""

    return EMail(
        subject="Version des DDB Images",
        sender="noreply@homeinfo.de",
        recipient=recipient,
        plain=get_template().format(filename=filename),
    )


def get_mailer() -> Mailer:
    """Return the automailer."""

    return Mailer.from_config(load_config("ddbfiles.conf"))


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument("filename", type=Path, help="name of the new file")
    return parser.parse_args()


def main() -> None:
    """Notify all stakeholders."""

    args = get_args()

    if match(DDB_ISO_REGEX, args.filename.name):
        notify(stakeholders("ddbfiles"), args.filename)
