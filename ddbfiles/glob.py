"""Re-usable glob."""

from pathlib import Path
from typing import Iterator, NamedTuple


__all__ = ['Glob']


class Glob(NamedTuple):
    """Re-usable glob."""

    path: Path
    glob: str

    def __iter__(self) -> Iterator[Path]:
        return self.path.glob(self.glob)
