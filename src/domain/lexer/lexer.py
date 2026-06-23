from __future__ import annotations
from ...shared.constants import EOF_CHAR
from ...shared.exceptions import UnterminatedCommentException
from ..protocols.char_stream import CharStream
from ..token.token import Token
from ..token.token_factory import TokenFactory
from ..token.atom_code import AtomCode
from .recognizers.token_recognizer import TokenRecognizer


class Lexer:
    """Domain Service — lê CharStream e produz o próximo Token."""

    def __init__(
        self,
        stream: CharStream,
        factory: TokenFactory,
        recognizers: list[TokenRecognizer],
    ) -> None:
        self._stream = stream
        self._factory = factory
        self._recognizers = recognizers

    def next_token(self) -> Token:
        self._skip_whitespace_and_comments()
        if not self._stream.has_next():
            return self._factory.create_eof(self._stream.current_line())
        ch = self._stream.peek()
        recognizer = self._find_recognizer(ch)
        if recognizer is not None:
            return recognizer.recognize(self._stream)
        self._stream.next()  # filtro 1º nível: char inválido descartado
        return self.next_token()

    def _find_recognizer(self, ch: str) -> TokenRecognizer | None:
        for rec in self._recognizers:
            if rec.can_handle(ch):
                return rec
        return None

    def _skip_whitespace_and_comments(self) -> None:
        while self._stream.has_next():
            ch = self._stream.peek()
            if ch in (" ", "\t", "\n", "\r"):
                self._stream.next()
            elif self._is_line_comment():
                self._skip_line_comment()
            elif self._is_block_comment():
                self._skip_block_comment()
            else:
                break

    def _is_line_comment(self) -> bool:
        return self._peek_two() == "//"

    def _is_block_comment(self) -> bool:
        return self._peek_two() == "/*"

    def _peek_two(self) -> str:
        if not self._stream.has_next():
            return ""
        first = self._stream.next()
        second = self._stream.peek() if self._stream.has_next() else EOF_CHAR
        self._stream.rewind()
        return first + second

    def _skip_line_comment(self) -> None:
        while self._stream.has_next() and self._stream.peek() != "\n":
            self._stream.next()

    def _skip_block_comment(self) -> None:
        open_line = self._stream.current_line()
        self._stream.next()  # /
        self._stream.next()  # *
        while self._stream.has_next():
            ch = self._stream.next()
            if ch == "*" and self._stream.has_next() and self._stream.peek() == "/":
                self._stream.next()
                return
        raise UnterminatedCommentException(open_line)
