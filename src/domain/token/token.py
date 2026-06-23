from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .atom_code import AtomCode


@dataclass(frozen=True)
class Token:
    """Value Object — imutável após criação."""

    code: AtomCode
    lexeme: str
    line: int
    symbol_index: Optional[int] = None

    def is_eof(self) -> bool:
        return self.code == AtomCode.EOF

    def is_identifier(self) -> bool:
        return self.code == AtomCode.IDENTIFIER

    def is_type_keyword(self) -> bool:
        type_codes = {
            AtomCode.REAL_KW,
            AtomCode.INTEGER_KW,
            AtomCode.STRING_KW,
            AtomCode.BOOLEAN_KW,
            AtomCode.CHARACTER_KW,
            AtomCode.VOID_KW,
        }
        return self.code in type_codes

    def __str__(self) -> str:
        return f"Token({self.code.value}, '{self.lexeme}', L{self.line})"
