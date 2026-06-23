from __future__ import annotations
from typing import Optional
from .symbol_entry import SymbolEntry
from .symbol_type import SymbolType
from ..token.atom_code import AtomCode


class SymbolTable:
    """Repository — busca O(1) por lexema + acesso O(1) por índice."""

    def __init__(self) -> None:
        self._lexeme_to_index: dict[str, int] = {}
        self._entries: list[SymbolEntry] = []

    def insert(
        self,
        lexeme: str,
        code: AtomCode,
        chars_before: int,
        chars_after: int,
        line: int,
    ) -> SymbolEntry:
        existing = self.find_by_lexeme(lexeme)
        if existing is not None:
            existing.add_line(line)
            return existing
        index = len(self._entries) + 1
        entry = SymbolEntry(
            index=index,
            code=code,
            lexeme=lexeme,
            chars_before_trunc=chars_before,
            chars_after_trunc=chars_after,
        )
        entry.add_line(line)
        self._entries.append(entry)
        self._lexeme_to_index[lexeme] = index
        return entry

    def find_by_lexeme(self, lexeme: str) -> Optional[SymbolEntry]:
        idx = self._lexeme_to_index.get(lexeme)
        if idx is None:
            return None
        return self._entries[idx - 1]

    def find_by_index(self, index: int) -> Optional[SymbolEntry]:
        if 1 <= index <= len(self._entries):
            return self._entries[index - 1]
        return None

    def set_type(self, lexeme: str, sym_type: SymbolType) -> None:
        entry = self.find_by_lexeme(lexeme)
        if entry is not None:
            entry.type = sym_type

    def get_all(self) -> list[SymbolEntry]:
        return list(self._entries)
