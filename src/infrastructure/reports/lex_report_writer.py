from __future__ import annotations
from pathlib import Path
from datetime import date
from ...domain.token.token import Token
from ...shared.constants import TEAM_NAME, TEAM_MEMBERS, LEX_EXTENSION


class LexReportWriter:
    """Builder — monta o relatório léxico em etapas."""

    def __init__(self, base_name: str, source_content: str) -> None:
        self._base_name = base_name
        self._source_content = source_content
        self._lines: list[str] = []

    def write(self, tokens: list[Token]) -> Path:
        self._build_header()
        self._build_source()
        self._build_body(tokens)
        return self._flush()

    def _build_header(self) -> None:
        self._lines += [
            "SENAI CIMATEC / EngComp / Compiladores",
            f"Equipe: {TEAM_NAME}",
            f"Membros: {TEAM_MEMBERS}",
            f"Arquivo: {self._base_name}.261",
            f"Data: {date.today().strftime('%d/%m/%Y')}",
            "",
            "=" * 60,
            "RELATÓRIO LÉXICO",
            "=" * 60,
            "",
        ]

    def _build_source(self) -> None:
        self._lines.append("FONTE ANALISADA:")
        self._lines.append("-" * 40)
        for i, line in enumerate(self._source_content.splitlines(), 1):
            self._lines.append(f"{i:4d} | {line}")
        self._lines += ["", "=" * 60, "TOKENS:", "-" * 60]
        self._lines.append(f"{'Linha':>6}  {'Código':<8}  Lexema")
        self._lines.append("-" * 60)

    def _build_body(self, tokens: list[Token]) -> None:
        for tok in tokens:
            self._lines.append(
                f"{tok.line:>6}  {tok.code.value:<8}  {tok.lexeme}"
            )

    def _flush(self) -> Path:
        path = Path(self._base_name).with_suffix(LEX_EXTENSION)
        path.write_text("\n".join(self._lines), encoding="utf-8")
        return path
