"""File type."""

from datetime import datetime
from pathlib import Path
from re import fullmatch
from typing import Iterable, Iterator, NamedTuple, Optional


__all__ = ['File', 'Version']


class Version(NamedTuple):
    """File version."""

    version: str
    path: Path


class File(NamedTuple):
    """Representation of a versioned file."""

    paths: Iterable[Path]
    regex: Optional[str] = None

    @property
    def versions(self) -> Iterator[Version]:
        """Yield versions of the given file."""
        if self.regex is None:
            return self._stat_versions()

        return self._regex_versions()

    def version(self, requested: str) -> Path:
        """Returns the requested version."""
        for version, path in self.versions:
            if version == requested:
                return path

        raise ValueError('No such version.')

    def _regex_versions(self) -> Iterator[Version]:
        """Yield versions by regular expression."""
        for path in self.paths:
            if match := fullmatch(self.regex, path.name):
                yield Version(match.group(1), path)

    def _stat_versions(self) -> Iterator[Version]:
        """Yield versions by modification time."""
        for path in self.paths:
            yield Version(
                datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                path
            )
