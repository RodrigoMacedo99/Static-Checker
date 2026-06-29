"""Composition Root — único ponto que monta o grafo de dependências."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

from .shared.constants import SOURCE_EXTENSION
from .shared.exceptions import LexException
from .domain.token.token_factory import TokenFactory
from .domain.symbol_table.symbol_table import SymbolTable
from .domain.symbol_table.reserved_words_table import ReservedWordsTable
from .domain.lexer.lexer import Lexer
from .domain.lexer.recognizers.identifier_recognizer import IdentifierRecognizer
from .domain.lexer.recognizers.number_recognizer import NumberRecognizer
from .domain.lexer.recognizers.string_recognizer import StringRecognizer
from .domain.lexer.recognizers.char_recognizer import CharRecognizer
from .domain.lexer.recognizers.symbol_recognizer import SymbolRecognizer
from .application.scope_manager import ScopeManager
from .application.static_checker_service import StaticCheckerService
from .infrastructure.io.file_reader import FileReader
from .infrastructure.reports.lex_report_writer import LexReportWriter
from .infrastructure.reports.tab_report_writer import TabReportWriter


def _parse_args() -> str:
    parser = argparse.ArgumentParser(description="Static Checker — BobEnzo2026-1")
    parser.add_argument("filename", help="Nome base do arquivo (sem extensão)")
    return parser.parse_args().filename


def _read_source(base_name: str) -> str:
    return Path(base_name).with_suffix(SOURCE_EXTENSION).read_text(encoding="utf-8")


def _build_service(base_name: str) -> StaticCheckerService:
    stream = FileReader().open(base_name)
    factory = TokenFactory()
    symbol_table = SymbolTable()
    reserved_table = ReservedWordsTable()
    recognizers = [
        IdentifierRecognizer(factory, symbol_table, reserved_table),
        NumberRecognizer(factory),
        StringRecognizer(factory),
        CharRecognizer(factory),
        SymbolRecognizer(factory),
    ]
    lexer = Lexer(stream, factory, recognizers)
    return StaticCheckerService(lexer, symbol_table, ScopeManager())


def main() -> None:
    base_name = "./source.261"
    try:
        service = _build_service(base_name)
        tokens = service.run()
        symbols = service.get_symbols()
        source = _read_source(base_name)

        lex_path = LexReportWriter(base_name, source).write(tokens)
        tab_path = TabReportWriter(base_name).write(symbols)

        print(f"OK — {len(tokens)} tokens, {len(symbols)} símbolos.")
        print(f"     {lex_path.name} e {tab_path.name} gerados.")
    except LexException as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)
