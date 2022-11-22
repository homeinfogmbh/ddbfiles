"""File type."""

from datetime import datetime
from pathlib import Path
from re import fullmatch
from typing import Iterable, Iterator, NamedTuple, Optional


__all__ = ['File']


class File(NamedTuple):
    """Representation of a versioned file."""

    paths: Iterable[Path]
    regex: Optional[str] = None

    @property
    def versions(self) -> Iterator[tuple[str, str]]:
        """Yield versions of the given file."""
        if self.regex is None:
            return self._stat_versions()

        return self._regex_versions()

    def version(self, requested: str) -> str:
        """Returns the requested version."""
        for version, file in self.versions:
            if version == requested:
                return file

        raise ValueError('No such version.')

    def _regex_versions(self) -> Iterator[tuple[str, str]]:
        """Yield versions by regular expression."""
        for path in self.paths:
            if match := fullmatch(self.regex, path.name):
                yield match.group(1), match.string

    def _stat_versions(self) -> Iterator[tuple[str, str]]:
        """Yield versions by modification time."""
        for path in self.paths:
            yield (
                datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                path.name
            )
