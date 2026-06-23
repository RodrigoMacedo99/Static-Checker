import pytest
from src.domain.token.token_factory import TokenFactory
from src.domain.token.atom_code import AtomCode
from src.domain.symbol_table.symbol_table import SymbolTable
from src.domain.symbol_table.reserved_words_table import ReservedWordsTable
from src.domain.lexer.recognizers.identifier_recognizer import IdentifierRecognizer
from src.infrastructure.io.double_buffer import DoubleBuffer


def _make_rec() -> IdentifierRecognizer:
    return IdentifierRecognizer(TokenFactory(), SymbolTable(), ReservedWordsTable())


def _recognize(source: str) -> tuple[AtomCode, str]:
    rec = _make_rec()
    tok = rec.recognize(DoubleBuffer(source))
    return tok.code, tok.lexeme


def test_simple_identifier():
    code, lex = _recognize("myvar ")
    assert code == AtomCode.IDENTIFIER
    assert lex == "MYVAR"


def test_underscore_start():
    code, lex = _recognize("_x1 ")
    assert code == AtomCode.IDENTIFIER
    assert lex == "_X1"


def test_reserved_word_program():
    code, lex = _recognize("program ")
    assert code == AtomCode.PROGRAM


def test_camelcase_reserved_word():
    # Palavras reservadas como "endDeclarations" têm camelCase: o reconhecedor
    # deve ler letras maiúsculas no interior do lexema (só o 1° char é lowercase).
    code, _ = _recognize("endDeclarations ")
    assert code == AtomCode.END_DECLARATIONS


def test_truncation_at_30():
    long_name = "a" * 40
    code, lex = _recognize(long_name + " ")
    assert code == AtomCode.IDENTIFIER
    assert len(lex) == 30


def test_same_identifier_returns_same_index():
    sym = SymbolTable()
    factory = TokenFactory()
    rec = IdentifierRecognizer(factory, sym, ReservedWordsTable())
    t1 = rec.recognize(DoubleBuffer("foo "))
    rec2 = IdentifierRecognizer(factory, sym, ReservedWordsTable())
    t2 = rec2.recognize(DoubleBuffer("foo "))
    assert t1.symbol_index == t2.symbol_index


def test_can_handle():
    rec = _make_rec()
    assert rec.can_handle("a")
    assert rec.can_handle("_")
    assert not rec.can_handle("A")
    assert not rec.can_handle("1")
