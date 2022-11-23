"""Notifications about file updates."""

from argparse import ArgumentParser, Namespace
from typing import Iterable

from configlib import load_config
from emaillib import EMail, Mailer
from functools import partial
from his import Account, stakeholders


__all__ = ['notify']


TEXT_TEMPLATE = '''Sehr geehrte Empfänger:innen,

es gibt neue DDB-Dateien zum herunter laden:
{filename}

Mit freundlichen Grüßen

Ihre HOMEINFO GmbH
'''


def notify(accounts: Iterable[Account], filename: str) -> None:
    """Notify the given accounts."""

    get_mailer().send(
        map(
            partial(generate_email, filename=filename),
            map(lambda account: account.email, accounts)
        )
    )


def generate_email(recipient: str, filename: str) -> EMail:
    """Yield emails for the respective recipients."""

    return EMail(
        subject='Neue DDB Dateien',
        sender='automailer@homeifno.de',
        recipient=recipient,
        plain=TEXT_TEMPLATE.format(filename=filename)
    )


def get_mailer() -> Mailer:
    """Return the automailer."""

    return Mailer.from_config(load_config('ddbfiles.conf'))


def get_args(description: str = __doc__) -> Namespace:
    """Return the parsed command line arguments."""

    parser = ArgumentParser(description=description)
    parser.add_argument('filename', help='name of the new file')
    return parser.parse_args()


def main() -> None:
    """Notify all stakeholders."""

    args = get_args()
    notify(stakeholders('ddbfiles'), args.filename)
