import pytest
from src.domain.symbol_table.symbol_table import SymbolTable
from src.domain.symbol_table.symbol_type import SymbolType
from src.domain.token.atom_code import AtomCode


def _table() -> SymbolTable:
    return SymbolTable()


def test_insert_and_find():
    t = _table()
    entry = t.insert("FOO", AtomCode.IDENTIFIER, 3, 3, 1)
    assert entry.index == 1
    assert entry.lexeme == "FOO"
    assert 1 in entry.lines


def test_duplicate_insert_adds_line():
    t = _table()
    t.insert("FOO", AtomCode.IDENTIFIER, 3, 3, 1)
    e2 = t.insert("FOO", AtomCode.IDENTIFIER, 3, 3, 5)
    assert 5 in e2.lines
    assert len(t.get_all()) == 1


def test_max_five_lines():
    t = _table()
    for line in range(1, 8):
        t.insert("BAR", AtomCode.IDENTIFIER, 3, 3, line)
    entry = t.find_by_lexeme("BAR")
    assert entry is not None
    assert len(entry.lines) == 5


def test_set_type():
    t = _table()
    t.insert("X", AtomCode.IDENTIFIER, 1, 1, 1)
    t.set_type("X", SymbolType.INTEGER)
    entry = t.find_by_lexeme("X")
    assert entry is not None
    assert entry.type == SymbolType.INTEGER


def test_find_by_index():
    t = _table()
    t.insert("A", AtomCode.IDENTIFIER, 1, 1, 1)
    t.insert("B", AtomCode.IDENTIFIER, 1, 1, 1)
    assert t.find_by_index(2) is not None
    assert t.find_by_index(2).lexeme == "B"  # type: ignore[union-attr]


def test_find_nonexistent_returns_none():
    t = _table()
    assert t.find_by_lexeme("NOPE") is None
    assert t.find_by_index(99) is None
