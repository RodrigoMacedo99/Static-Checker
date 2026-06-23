import pytest
from src.domain.token.token_factory import TokenFactory
from src.domain.token.atom_code import AtomCode
from src.domain.symbol_table.symbol_table import SymbolTable
from src.domain.symbol_table.reserved_words_table import ReservedWordsTable
from src.domain.lexer.lexer import Lexer
from src.domain.lexer.recognizers.identifier_recognizer import IdentifierRecognizer
from src.domain.lexer.recognizers.number_recognizer import NumberRecognizer
from src.domain.lexer.recognizers.string_recognizer import StringRecognizer
from src.domain.lexer.recognizers.char_recognizer import CharRecognizer
from src.domain.lexer.recognizers.symbol_recognizer import SymbolRecognizer
from src.infrastructure.io.double_buffer import DoubleBuffer
from src.shared.exceptions import UnterminatedCommentException


def _make_lexer(source: str) -> Lexer:
    stream = DoubleBuffer(source)
    factory = TokenFactory()
    sym = SymbolTable()
    reserved = ReservedWordsTable()
    recs = [
        IdentifierRecognizer(factory, sym, reserved),
        NumberRecognizer(factory),
        StringRecognizer(factory),
        CharRecognizer(factory),
        SymbolRecognizer(factory),
    ]
    return Lexer(stream, factory, recs)


def _tokens(source: str) -> list[AtomCode]:
    lexer = _make_lexer(source)
    result = []
    while True:
        tok = lexer.next_token()
        result.append(tok.code)
        if tok.is_eof():
            break
    return result


def test_skip_line_comment():
    codes = _tokens("// comentario\nprogram")
    assert AtomCode.PROGRAM in codes


def test_skip_block_comment():
    codes = _tokens("/* bloco */ program")
    assert codes[0] == AtomCode.PROGRAM


def test_unterminated_block_comment():
    with pytest.raises(UnterminatedCommentException):
        _tokens("/* sem fechamento")


def test_assignment_operator():
    codes = _tokens(":=")
    assert AtomCode.ASSIGN in codes


def test_array_decl_token():
    codes = _tokens("[]")
    assert AtomCode.ARRAY_DECL in codes


def test_bracket_separate():
    codes = _tokens("[42]")
    assert AtomCode.LBRACKET in codes
    assert AtomCode.RBRACKET in codes


def test_if_uppercase():
    codes = _tokens("If")
    assert AtomCode.IF_UPPER in codes


def test_full_program_tokens():
    src = "program myprog declarations endDeclarations endProgram"
    codes = _tokens(src)
    assert AtomCode.PROGRAM in codes
    assert AtomCode.DECLARATIONS in codes
    assert AtomCode.END_DECLARATIONS in codes
    assert AtomCode.END_PROGRAM in codes


def test_eof_at_empty_source():
    codes = _tokens("")
    assert codes == [AtomCode.EOF]
