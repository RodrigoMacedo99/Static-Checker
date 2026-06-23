from __future__ import annotations
from ...protocols.char_stream import CharStream
from ...token.token import Token
from ...token.token_factory import TokenFactory
from ....shared.constants import EOF_CHAR
from .token_recognizer import TokenRecognizer

# Apenas letras minúsculas são válidas como CharacterLiteral (ver BRUT_OTIM CH1)
_VALID_CHARS: frozenset[str] = frozenset("abcdefghijklmnopqrstuvwxyz")


class CharRecognizer(TokenRecognizer):
    """Autômato CH0→CH3: '\\'' Letter '\\''.
    Dígitos entre aspas simples são inválidos — só Letter é aceita."""

    def __init__(self, factory: TokenFactory) -> None:
        self._factory = factory

    def can_handle(self, ch: str) -> bool:
        return ch == "'"

    def recognize(self, stream: CharStream) -> Token:
        line = stream.current_line()
        stream.next()  # consome aspa de abertura
        letter = self._read_letter(stream)
        self._consume_closing_quote(stream)
        return self._factory.create_char(f"'{letter}'", line)

    def _read_letter(self, stream: CharStream) -> str:
        ch = stream.peek() if stream.has_next() else EOF_CHAR
        if ch in _VALID_CHARS:
            return stream.next()
        # char inválido: consome e usa placeholder (filtro de 1º nível)
        if stream.has_next():
            stream.next()
        return "?"

    def _consume_closing_quote(self, stream: CharStream) -> None:
        if stream.has_next() and stream.peek() == "'":
            stream.next()
