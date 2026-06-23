from __future__ import annotations
from ...protocols.char_stream import CharStream
from ...token.token import Token
from ...token.token_factory import TokenFactory
from ...token.atom_code import AtomCode
from ....shared.constants import EOF_CHAR
from .token_recognizer import TokenRecognizer

_SINGLE: dict[str, AtomCode] = {
    ";": AtomCode.SEMICOLON, "(": AtomCode.LPAREN, ")": AtomCode.RPAREN,
    "]": AtomCode.RBRACKET, "{": AtomCode.LBRACE, "}": AtomCode.RBRACE,
    "#": AtomCode.HASH, "+": AtomCode.PLUS, "-": AtomCode.MINUS,
    "*": AtomCode.STAR, "%": AtomCode.PERCENT, ",": AtomCode.COMMA,
    "?": AtomCode.QUESTION,
}


class SymbolRecognizer(TokenRecognizer):
    def __init__(self, factory: TokenFactory) -> None:
        self._factory = factory

    def can_handle(self, ch: str) -> bool:
        return not (ch.islower() or ch.isdigit() or ch in {'"', "'", " ", "\t", "\n", "\r"})

    def recognize(self, stream: CharStream) -> Token:
        line = stream.current_line()
        ch = stream.next()
        return self._dispatch(ch, stream, line)

    def _dispatch(self, ch: str, stream: CharStream, line: int) -> Token:
        if ch in _SINGLE:
            return self._factory.create_symbol(_SINGLE[ch], ch, line)
        if ch == ":":
            return self._handle_colon(stream, line)
        if ch == "<":
            return self._handle_lt(stream, line)
        if ch == ">":
            return self._handle_gt(stream, line)
        if ch == "=":
            return self._handle_eq(stream, line)
        if ch == "!":
            return self._handle_neq(stream, line)
        if ch == "[":
            return self._handle_lbracket(stream, line)
        if ch == "I":
            return self._handle_upper_i(stream, line)
        if ch == "/":
            return self._factory.create_symbol(AtomCode.SLASH, "/", line)
        return self._factory.create_symbol(AtomCode.EOF, ch, line)  # char inválido filtrado

    def _handle_colon(self, stream: CharStream, line: int) -> Token:
        if stream.has_next() and stream.peek() == "=":
            stream.next()
            return self._factory.create_symbol(AtomCode.ASSIGN, ":=", line)
        return self._factory.create_symbol(AtomCode.COLON, ":", line)

    def _handle_lt(self, stream: CharStream, line: int) -> Token:
        if stream.has_next() and stream.peek() == "=":
            stream.next()
            return self._factory.create_symbol(AtomCode.LE, "<=", line)
        return self._factory.create_symbol(AtomCode.LT, "<", line)

    def _handle_gt(self, stream: CharStream, line: int) -> Token:
        if stream.has_next() and stream.peek() == "=":
            stream.next()
            return self._factory.create_symbol(AtomCode.GE, ">=", line)
        return self._factory.create_symbol(AtomCode.GT, ">", line)

    def _handle_eq(self, stream: CharStream, line: int) -> Token:
        if stream.has_next() and stream.peek() == "=":
            stream.next()
            return self._factory.create_symbol(AtomCode.EQ, "==", line)
        return self._factory.create_symbol(AtomCode.EOF, "=", line)

    def _handle_neq(self, stream: CharStream, line: int) -> Token:
        if stream.has_next() and stream.peek() == "=":
            stream.next()
            return self._factory.create_symbol(AtomCode.NEQ, "!=", line)
        return self._factory.create_symbol(AtomCode.EOF, "!", line)

    def _handle_lbracket(self, stream: CharStream, line: int) -> Token:
        if stream.has_next() and stream.peek() == "]":
            stream.next()
            return self._factory.create_symbol(AtomCode.ARRAY_DECL, "[]", line)
        return self._factory.create_symbol(AtomCode.LBRACKET, "[", line)

    def _handle_upper_i(self, stream: CharStream, line: int) -> Token:
        # "If" é o único token com maiúscula na linguagem BobEnzo2026-1
        if stream.has_next() and stream.peek() == "f":
            stream.next()
            return self._factory.create_symbol(AtomCode.IF_UPPER, "If", line)
        return self._factory.create_symbol(AtomCode.EOF, "I", line)
