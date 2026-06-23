from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .symbol_type import SymbolType
from ..token.atom_code import AtomCode
from ...shared.constants import MAX_SYMBOL_LINES


@dataclass
class SymbolEntry:
    """Entity — identidade dada pelo index."""

    index: int           # imutável
    code: AtomCode       # imutável
    lexeme: str          # imutável, uppercase, max 30 chars
    chars_before_trunc: int
    chars_after_trunc: int
    type: Optional[SymbolType] = None
    lines: list[int] = field(default_factory=list)

    def add_line(self, line: int) -> None:
        if line not in self.lines and len(self.lines) < MAX_SYMBOL_LINES:
            self.lines.append(line)

    def lines_str(self) -> str:
        return ", ".join(str(ln) for ln in self.lines)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolEntry):
            return NotImplemented
        return self.index == other.index

    def __hash__(self) -> int:
        return hash(self.index)
