from __future__ import annotations
from ...protocols.char_stream import CharStream
from ...token.token import Token
from ...token.token_factory import TokenFactory
from ....shared.constants import EOF_CHAR
from ....shared.exceptions import UnterminatedStringException
from .token_recognizer import TokenRecognizer

# StringChar válidos conforme gramática: Letter | Digit | '$' | '_' | '.' | ' '
_STRING_CHARS: frozenset[str] = frozenset(
    "abcdefghijklmnopqrstuvwxyz0123456789$_. "
)


class StringRecognizer(TokenRecognizer):
    """Autômato SL0→SL3: '\"' StringChar { StringChar } '\"'.
    Rejeita string vazia — SL1 não é estado final (ver BRUT_OTIM)."""

    def __init__(self, factory: TokenFactory) -> None:
        self._factory = factory

    def can_handle(self, ch: str) -> bool:
        return ch == '"'

    def recognize(self, stream: CharStream) -> Token:
        line = stream.current_line()
        stream.next()  # consome a aspa de abertura
        content = self._read_content(stream, line)
        return self._factory.create_string(f'"{content}"', line)

    def _read_content(self, stream: CharStream, open_line: int) -> str:
        buf: list[str] = []
        has_char = False
        while True:
            ch = stream.peek() if stream.has_next() else EOF_CHAR
            if ch == EOF_CHAR or ch == "\n":
                raise UnterminatedStringException(open_line)
            if ch == '"':
                if not has_char:
                    # SL1 não é estado final: string vazia é inválida;
                    # consome a aspa e sinaliza string vazia como erro
                    stream.next()
                    raise UnterminatedStringException(open_line)
                stream.next()  # consome aspa de fechamento
                return "".join(buf)
            if ch in _STRING_CHARS:
                buf.append(stream.next())
                has_char = True
            else:
                stream.next()  # filtro de 1º nível: char inválido descartado
