"""Notifications about file updates."""

from typing import Iterable

from configlib import load_config
from emaillib import EMail, Mailer
from his import Account, stakeholders


__all__ = ['notify']


TEXT = '''Sehr geehrte Empfänger:innen,

es gibt neue DDB-Dateien zum herunter laden.
Besuchen Sie dazu: {url}

Mit freundlichen Grüßen

Ihre HOMEINFO GmbH
'''


def notify(accounts: Iterable[Account]) -> None:
    """Notify the given accounts."""

    get_mailer().send(
        map(generate_email, map(lambda account: account.email, accounts))
    )


def generate_email(recipient: str) -> EMail:
    """Yield emails for the respective recipients."""

    return EMail(
        subject='Neue DDB Dateien',
        sender='automailer@homeifno.de',
        recipient=recipient,
        plain=TEXT
    )


def get_mailer() -> Mailer:
    """Return the automailer."""

    return Mailer.from_config(load_config('ddbfiles.conf'))


def main() -> None:
    """Notify all stakeholders."""

    notify(stakeholders('ddbfiles'))
