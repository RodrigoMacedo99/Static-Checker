from __future__ import annotations
from pathlib import Path
from ...shared.constants import BUFFER_SIZE, EOF_CHAR


class DoubleBuffer:
    """Implementação concreta do CharStream com buffer duplo clássico."""

    def __init__(self, content: str) -> None:
        self._content = content
        self._pos: int = 0
        self._line: int = 1

    @classmethod
    def from_path(cls, path: Path) -> "DoubleBuffer":
        return cls(path.read_text(encoding="utf-8"))

    def has_next(self) -> bool:
        return self._pos < len(self._content)

    def next(self) -> str:
        if not self.has_next():
            return EOF_CHAR
        ch = self._content[self._pos]
        self._pos += 1
        if ch == "\n":
            self._line += 1
        return ch

    def peek(self) -> str:
        if not self.has_next():
            return EOF_CHAR
        return self._content[self._pos]

    def rewind(self) -> None:
        if self._pos > 0:
            self._pos -= 1
            if self._content[self._pos] == "\n":
                self._line -= 1

    def current_line(self) -> int:
        return self._line
