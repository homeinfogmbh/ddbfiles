"""Notifications about file updates."""

from argparse import ArgumentParser, Namespace
from functools import partial
from typing import Iterable

from configlib import load_config
from emaillib import EMail, Mailer
from his import Account, stakeholders

__all__ = ['notify']


DOWNLOAD_URL = 'https://sysmon2.homeinfo.de/dashboard.html '
TEXT_TEMPLATE = f'''Sehr geehrte Empfänger:innen,

es gibt eine neu DDB-Datei zum herunter laden:

* {{filename}}

Sie können die Datei unter {DOWNLOAD_URL}
herunter laden.

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
        sender='noreply@homeinfo.de',
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
