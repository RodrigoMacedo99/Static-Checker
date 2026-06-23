from __future__ import annotations
from pathlib import Path
from datetime import date
from ...domain.symbol_table.symbol_entry import SymbolEntry
from ...shared.constants import TEAM_NAME, TEAM_MEMBERS, TAB_EXTENSION


class TabReportWriter:
    """Builder — monta o relatório da tabela de símbolos."""

    def __init__(self, base_name: str) -> None:
        self._base_name = base_name
        self._lines: list[str] = []

    def write(self, entries: list[SymbolEntry]) -> Path:
        self._build_header()
        self._build_body(entries)
        return self._flush()

    def _build_header(self) -> None:
        self._lines += [
            "SENAI CIMATEC / EngComp / Compiladores",
            f"Equipe: {TEAM_NAME}",
            f"Membros: {TEAM_MEMBERS}",
            f"Arquivo: {self._base_name}.261",
            f"Data: {date.today().strftime('%d/%m/%Y')}",
            "",
            "=" * 70,
            "TABELA DE SÍMBOLOS",
            "=" * 70,
            "",
            f"{'Índice':>6}  {'Código':<8}  {'Lexema':<32}  {'Tipo':<6}  {'Linhas'}",
            "-" * 70,
        ]

    def _build_body(self, entries: list[SymbolEntry]) -> None:
        for entry in entries:
            tipo = entry.type.value if entry.type else "---"
            self._lines.append(
                f"{entry.index:>6}  {entry.code.value:<8}  "
                f"{entry.lexeme:<32}  {tipo:<6}  {entry.lines_str()}"
            )

    def _flush(self) -> Path:
        path = Path(self._base_name).with_suffix(TAB_EXTENSION)
        path.write_text("\n".join(self._lines), encoding="utf-8")
        return path
