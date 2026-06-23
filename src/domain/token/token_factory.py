from __future__ import annotations
from typing import Optional
from .atom_code import AtomCode
from .token import Token
from ..shared_types import TruncatedLexeme


class TokenFactory:
    """Factory — encapsula invariantes de construção de Token por categoria."""

    def create_identifier(
        self,
        truncated: TruncatedLexeme,
        line: int,
        symbol_index: int,
    ) -> Token:
        return Token(AtomCode.IDENTIFIER, truncated.stored, line, symbol_index)

    def create_reserved_word(
        self,
        code: AtomCode,
        lexeme: str,
        line: int,
    ) -> Token:
        return Token(code, lexeme.upper(), line)

    def create_number(
        self,
        code: AtomCode,
        lexeme: str,
        line: int,
    ) -> Token:
        return Token(code, lexeme, line)

    def create_string(self, lexeme: str, line: int) -> Token:
        return Token(AtomCode.STRING_LIT, lexeme, line)

    def create_char(self, lexeme: str, line: int) -> Token:
        return Token(AtomCode.CHAR_LIT, lexeme, line)

    def create_symbol(self, code: AtomCode, lexeme: str, line: int) -> Token:
        return Token(code, lexeme, line)

    def create_eof(self, line: int) -> Token:
        return Token(AtomCode.EOF, "", line)
