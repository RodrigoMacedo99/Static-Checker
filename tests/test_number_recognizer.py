import pytest
from src.domain.token.token_factory import TokenFactory
from src.domain.token.atom_code import AtomCode
from src.domain.lexer.recognizers.number_recognizer import NumberRecognizer
from src.infrastructure.io.double_buffer import DoubleBuffer


def _recognize(source: str) -> tuple[AtomCode, str]:
    stream = DoubleBuffer(source)
    rec = NumberRecognizer(TokenFactory())
    tok = rec.recognize(stream)
    return tok.code, tok.lexeme


def test_integer():
    code, lex = _recognize("42 ")
    assert code == AtomCode.INTEGER_LIT
    assert lex == "42"


def test_real():
    code, lex = _recognize("3.14 ")
    assert code == AtomCode.REAL_LIT
    assert lex == "3.14"


def test_scientific_no_sign():
    code, lex = _recognize("1.5e10 ")
    assert code == AtomCode.SCIENTIFIC_LIT
    assert lex == "1.5e10"


def test_scientific_plus():
    code, lex = _recognize("2.0e+3 ")
    assert code == AtomCode.SCIENTIFIC_LIT
    assert lex == "2.0e+3"


def test_scientific_minus():
    code, lex = _recognize("9.9e-2 ")
    assert code == AtomCode.SCIENTIFIC_LIT
    assert lex == "9.9e-2"


def test_integer_stops_at_dot_when_no_digit_follows():
    # "3." — ponto sem dígito depois não é Real; o autômato para em N1
    stream = DoubleBuffer("3.x")
    rec = NumberRecognizer(TokenFactory())
    tok = rec.recognize(stream)
    assert tok.code == AtomCode.INTEGER_LIT
    assert tok.lexeme == "3"


def test_can_handle_digit():
    rec = NumberRecognizer(TokenFactory())
    assert rec.can_handle("0")
    assert rec.can_handle("9")
    assert not rec.can_handle("a")
    assert not rec.can_handle(".")
