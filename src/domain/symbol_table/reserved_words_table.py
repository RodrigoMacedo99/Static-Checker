from types import MappingProxyType
from ..token.atom_code import AtomCode

_RAW: dict[str, AtomCode] = {
    "PROGRAM": AtomCode.PROGRAM,
    "ENDPROGRAM": AtomCode.END_PROGRAM,
    "DECLARATIONS": AtomCode.DECLARATIONS,
    "ENDDECLARATIONS": AtomCode.END_DECLARATIONS,
    "FUNCTIONS": AtomCode.FUNCTIONS,
    "ENDFUNCTIONS": AtomCode.END_FUNCTIONS,
    "FUNCTYPE": AtomCode.FUNC_TYPE,
    "VARTYPE": AtomCode.VAR_TYPE,
    "PARAMTYPE": AtomCode.PARAM_TYPE,
    "REAL": AtomCode.REAL_KW,
    "INTEGER": AtomCode.INTEGER_KW,
    "STRING": AtomCode.STRING_KW,
    "BOOLEAN": AtomCode.BOOLEAN_KW,
    "CHARACTER": AtomCode.CHARACTER_KW,
    "VOID": AtomCode.VOID_KW,
    "IF": AtomCode.IF_LOWER,
    "ELSE": AtomCode.ELSE,
    "ENDIF": AtomCode.END_IF,
    "WHILE": AtomCode.WHILE,
    "ENDWHILE": AtomCode.END_WHILE,
    "RETURN": AtomCode.RETURN,
    "BREAK": AtomCode.BREAK,
    "PRINT": AtomCode.PRINT,
    "TRUE": AtomCode.TRUE,
    "FALSE": AtomCode.FALSE,
}


class ReservedWordsTable:
    """Repository imutável carregado na inicialização."""

    def __init__(self) -> None:
        self._words: MappingProxyType[str, AtomCode] = MappingProxyType(_RAW)

    def lookup(self, lexeme: str) -> AtomCode | None:
        return self._words.get(lexeme.upper())

    def is_reserved(self, lexeme: str) -> bool:
        return lexeme.upper() in self._words
