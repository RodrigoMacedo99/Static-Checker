from __future__ import annotations
from ...protocols.char_stream import CharStream
from ...token.token import Token
from ...token.token_factory import TokenFactory
from ...token.atom_code import AtomCode
from ....shared.constants import EOF_CHAR
from .token_recognizer import TokenRecognizer

# Autômato N0-N6 implementado em nível léxico para evitar ambiguidade
# entre Integer, Real e Scientific (ver BRUT_OTIM, regra Number).
_STATE_ACCEPT: set[int] = {1, 3, 6}


class NumberRecognizer(TokenRecognizer):
    def __init__(self, factory: TokenFactory) -> None:
        self._factory = factory

    def can_handle(self, ch: str) -> bool:
        return ch.isdigit()

    def recognize(self, stream: CharStream) -> Token:
        line = stream.current_line()
        lexeme, final_state = self._run_automaton(stream)
        code = self._state_to_code(final_state)
        return self._factory.create_number(code, lexeme, line)

    def _run_automaton(self, stream: CharStream) -> tuple[str, int]:
        buf: list[str] = []
        state = 0
        while True:
            ch = stream.peek() if stream.has_next() else EOF_CHAR
            next_state = self._transition(state, ch)
            if next_state == -1:
                break
            # Lookahead: antes de aceitar '.' (N1→N2) ou 'e' (N3→N4),
            # confirma que o char seguinte é válido. Estado só avança se
            # o lookahead confirmar — "3.x" retorna INTEGER "3", não consome '.'.
            if state == 1 and ch == ".":
                buf.append(stream.next())
                after = stream.peek() if stream.has_next() else EOF_CHAR
                if not after.isdigit():
                    stream.rewind()
                    buf.pop()
                    break
                state = next_state
            elif state == 3 and ch == "e":
                buf.append(stream.next())
                after = stream.peek() if stream.has_next() else EOF_CHAR
                if not (after.isdigit() or after in ("+", "-")):
                    stream.rewind()
                    buf.pop()
                    break
                state = next_state
            else:
                buf.append(stream.next())
                state = next_state
        return "".join(buf), state

    def _transition(self, state: int, ch: str) -> int:
        if state == 0 and ch.isdigit():
            return 1
        if state == 1 and ch.isdigit():
            return 1
        if state == 1 and ch == ".":
            return 2
        if state == 2 and ch.isdigit():
            return 3
        if state == 3 and ch.isdigit():
            return 3
        if state == 3 and ch == "e":
            return 4
        if state == 4 and ch in ("+", "-"):
            return 5
        if state == 4 and ch.isdigit():
            return 6
        if state == 5 and ch.isdigit():
            return 6
        if state == 6 and ch.isdigit():
            return 6
        return -1

    def _state_to_code(self, state: int) -> AtomCode:
        if state == 1:
            return AtomCode.INTEGER_LIT
        if state == 3:
            return AtomCode.REAL_LIT
        return AtomCode.SCIENTIFIC_LIT
