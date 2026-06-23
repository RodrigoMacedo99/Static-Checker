from __future__ import annotations
from ..domain.lexer.lexer import Lexer
from ..domain.token.token import Token
from ..domain.token.atom_code import AtomCode
from ..domain.symbol_table.symbol_table import SymbolTable
from ..domain.symbol_table.symbol_type import SymbolType
from .scope_manager import ScopeManager

_SCOPE_ENTER = {AtomCode.DECLARATIONS: "declarations", AtomCode.FUNCTIONS: "functions"}
_SCOPE_EXIT = {AtomCode.END_DECLARATIONS, AtomCode.END_FUNCTIONS}

_TYPE_MAP: dict[AtomCode, SymbolType] = {
    AtomCode.REAL_KW: SymbolType.REAL,
    AtomCode.INTEGER_KW: SymbolType.INTEGER,
    AtomCode.STRING_KW: SymbolType.STRING,
    AtomCode.BOOLEAN_KW: SymbolType.BOOLEAN,
    AtomCode.CHARACTER_KW: SymbolType.CHARACTER,
    AtomCode.VOID_KW: SymbolType.VOID,
}


class StaticCheckerService:
    """Application Service — orquestra Lexer, SymbolTable e ScopeManager."""

    def __init__(
        self,
        lexer: Lexer,
        symbol_table: SymbolTable,
        scope_manager: ScopeManager,
    ) -> None:
        self._lexer = lexer
        self._symbol_table = symbol_table
        self._scope = scope_manager
        self._tokens: list[Token] = []

    def run(self) -> list[Token]:
        self._scope.enter_scope("global")
        pending_type: SymbolType | None = None
        is_array = False
        while True:
            tok = self._lexer.next_token()
            self._tokens.append(tok)
            if tok.is_eof():
                break
            pending_type, is_array = self._process_token(tok, pending_type, is_array)
        return self._tokens

    def _process_token(
        self,
        tok: Token,
        pending_type: SymbolType | None,
        is_array: bool,
    ) -> tuple[SymbolType | None, bool]:
        self._update_scope(tok)
        if tok.is_type_keyword():
            return _TYPE_MAP[tok.code], False
        if tok.code == AtomCode.ARRAY_DECL and pending_type is not None:
            return pending_type, True
        if tok.is_identifier() and pending_type is not None:
            self._apply_type(tok.lexeme, pending_type, is_array)
        if tok.code in {AtomCode.SEMICOLON, AtomCode.END_DECLARATIONS}:
            return None, False
        return pending_type, is_array

    def _update_scope(self, tok: Token) -> None:
        if tok.code in _SCOPE_ENTER:
            self._scope.enter_scope(_SCOPE_ENTER[tok.code])
        elif tok.code in _SCOPE_EXIT:
            self._scope.exit_scope()
        elif tok.code == AtomCode.FUNC_TYPE:
            self._scope.enter_scope("function")

    def _apply_type(self, lexeme: str, base: SymbolType, is_array: bool) -> None:
        resolved = self._array_type(base) if is_array else base
        self._symbol_table.set_type(lexeme, resolved)

    def _array_type(self, base: SymbolType) -> SymbolType:
        mapping = {
            SymbolType.REAL: SymbolType.ARRAY_REAL,
            SymbolType.INTEGER: SymbolType.ARRAY_INTEGER,
            SymbolType.STRING: SymbolType.ARRAY_STRING,
            SymbolType.CHARACTER: SymbolType.ARRAY_CHARACTER,
            SymbolType.BOOLEAN: SymbolType.ARRAY_BOOLEAN,
        }
        return mapping.get(base, base)

    @property
    def tokens(self) -> list[Token]:
        return list(self._tokens)

    def get_symbols(self) -> list:
        return self._symbol_table.get_all()
