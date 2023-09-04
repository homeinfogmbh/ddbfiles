"""Available files."""

from pathlib import Path

from ddbfiles.file import File
from ddbfiles.glob import Glob

__all__ = ["DDB_ISO_REGEX", "FILES"]


BASEDIR = Path("/usr/local/share/ddbfiles")
DDB_ISO_REGEX = r"HIDSL-(.+)-x86_64\.iso"
DDBOS_ISO_REGEX = r"DDBOS-(.+)-x86_64\.iso"
FILES = {
    "HIDSL": File(Glob(BASEDIR, "HIDSL-*-x86_64.iso"), DDB_ISO_REGEX),
    "DDBOS": File(Glob(BASEDIR, "DDBOS-*-x86_64.iso"), DDBOS_ISO_REGEX),
    "HIDSL-ARM": File(
        Glob(BASEDIR, "HIDSL-arm-raspi4-*.tar.lzop"),
        r"HIDSL-arm-raspi4-(.+)\.tar\.lzop",
    ),
    "manual": File([BASEDIR / "Installationsanleitung_DDB.pdf"]),
}
