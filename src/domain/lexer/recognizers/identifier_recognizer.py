from __future__ import annotations
from ...protocols.char_stream import CharStream
from ...token.token import Token
from ...token.token_factory import TokenFactory
from ...symbol_table.symbol_table import SymbolTable
from ...symbol_table.reserved_words_table import ReservedWordsTable
from ...shared_types import truncate
from ...token.atom_code import AtomCode
from .token_recognizer import TokenRecognizer


class IdentifierRecognizer(TokenRecognizer):
    """Automato ID0->ID1: ( Letter | '_' ) { Letter | Digit | '_' }."""

    def __init__(
        self,
        factory: TokenFactory,
        symbol_table: SymbolTable,
        reserved_table: ReservedWordsTable,
    ) -> None:
        self._factory = factory
        self._symbol_table = symbol_table
        self._reserved_table = reserved_table

    def can_handle(self, ch: str) -> bool:
        return ch.isalpha() or ch == "_"

    def recognize(self, stream: CharStream) -> Token:
        line = stream.current_line()
        lexeme = self._read_lexeme(stream)
        if lexeme == "If":
            return self._factory.create_reserved_word(AtomCode.IF_UPPER, lexeme, line)
        reserved_code = self._reserved_table.lookup(lexeme)
        if reserved_code is not None:
            return self._factory.create_reserved_word(reserved_code, lexeme, line)
        return self._make_identifier_token(lexeme, line)

    def _read_lexeme(self, stream: CharStream) -> str:
        buf: list[str] = []
        while stream.has_next():
            ch = stream.peek()
            if ch.isalpha() or ch.isdigit() or ch == "_":
                buf.append(stream.next())
            else:
                break
        return "".join(buf)

    def _make_identifier_token(self, raw: str, line: int) -> Token:
        truncated = truncate(raw)
        entry = self._symbol_table.insert(
            lexeme=truncated.stored,
            code=AtomCode.IDENTIFIER,
            chars_before=truncated.chars_before,
            chars_after=truncated.chars_after,
            line=line,
        )
        return self._factory.create_identifier(truncated, line, entry.index)
