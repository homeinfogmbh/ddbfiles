"""File type."""

from datetime import datetime
from pathlib import Path
from re import fullmatch
from typing import Iterable, Iterator, NamedTuple, Optional


__all__ = ['File']


NO_SUCH_VERSION = ValueError('No such version.')


class File(NamedTuple):
    """Representation of a versioned file."""

    paths: Iterable[Path]
    regex: Optional[str] = None

    @property
    def versions(self) -> Iterator[str]:
        """Yield versions of the given file."""
        if self.regex is None:
            return self._stat_versions()

        return self._regex_versions()

    def version(self, version: Optional[str] = None) -> str:
        """Returns the requested version."""
        if self.regex is None:
            if version is not None:
                raise NO_SUCH_VERSION

            return self._latest_version()

        if version is None:
            raise NO_SUCH_VERSION

        return self._requested_version(version)

    def _regex_versions(self) -> Iterator[str]:
        """Yield versions by regular expression."""
        for path in self.paths:
            if match := fullmatch(self.regex, path.name):
                yield match.group(1)

    def _stat_versions(self) -> Iterator[str]:
        """Yield versions by modification time."""
        for path in self.paths:
            yield datetime.fromtimestamp(path.stat().st_mtime).isoformat()

    def _latest_version(self) -> str:
        """Returns the latest version."""
        for path in self.paths:
            return path.name

        raise NO_SUCH_VERSION

    def _requested_version(self, version: str) -> str:
        """Return the requested file version."""
        for path in self.paths:
            if match := fullmatch(self.regex, path.name):
                if match.group(1) == version:
                    return match.string

        raise NO_SUCH_VERSION
