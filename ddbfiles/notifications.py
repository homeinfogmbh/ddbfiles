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

__all__ = ['notify']


TEXT_TEMPLATE = '''Sehr geehrte Damen und Herren, 

wir freuen uns, Ihnen mitteilen zu können, dass die neueste Version unseres DDB Images jetzt zum Download bereitsteht. 

Wir haben neue Funktionen hinzugefügt, die Ihnen mehr Flexibilität und Kontrolle bieten. Wenn Sie bereits eine vorherige Version des DDB Images verwenden, empfehlen wir Ihnen, dieses Update so bald wie möglich herunterzuladen.  

Die aktuelle Version ist: {filename}
Zum Download loggen Sie sich bitte im Sysmon unter folgendem Link ein: und finden Sie das Image dort im Bereich Download auf der Dashboard Seite 
https://sysmon2.homeinfo.de/dashboard.html

Vielen Dank für Ihr Interesse an unserem Produkt. Wir freuen uns auf Ihre Rückmeldungen und Fragen. 

Mit freundlichen Grüßen, 
HOMEINFO 
Digitale Informationssysteme GmbH 
Spörckenstr. 11 

30419 Hannover 

Fon.: 0511 21 24 11 00 
Web : www.homeinfo.de

Amtsgericht Hannover HRB 58516 
Ust - IDNr.:  DE 206025922 
Geschäftsführer: 
Marcus Berbic 
Patrick Gunkel
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
        subject='Version des DDB Images',
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
    parser.add_argument('filename', type=Path, help='name of the new file')
    return parser.parse_args()


def main() -> None:
    """Notify all stakeholders."""

    args = get_args()

    if match(DDB_ISO_REGEX, args.filename.name):
        notify(stakeholders('ddbfiles'), args.filename)
