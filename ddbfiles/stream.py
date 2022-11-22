"""File streaming."""

from pathlib import Path
from typing import Iterator


__all__ = ['stream']


def stream(path: Path, *, chunk_size: int = 4096) -> Iterator[bytes]:
    """Yields chunks of a file."""

    with path.open('rb') as file:
        while chunk := file.read(chunk_size):
            yield chunk
