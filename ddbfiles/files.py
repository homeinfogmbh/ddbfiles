"""Available files."""

from pathlib import Path

from ddbfiles.file import File
from ddbfiles.glob import Glob

__all__ = ['FILES']


BASEDIR = Path('/usr/local/share/ddbfiles')
FILES = {
    'HIDSL': File(
        Glob(BASEDIR, 'HIDSL-*-x86_64.iso'),
        r'HIDSL-(.+)-x86_64\.iso'
    ),
    'HIDSL-ARM': File(
        Glob(BASEDIR, 'HIDSL-arm-raspi4-*.tar.lzop'),
        r'HIDSL-arm-raspi4-(.+)\.tar\.lzop'
    ),
    'manual': File([BASEDIR / 'Installationsanleitung_DDB.pdf'])
}
