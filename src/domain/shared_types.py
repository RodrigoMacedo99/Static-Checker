from dataclasses import dataclass
from ..shared.constants import MAX_LEXEME_LENGTH


@dataclass(frozen=True)
class TruncatedLexeme:
    """Resultado do processo de leitura e truncagem de um lexema."""

    stored: str        # uppercase, max MAX_LEXEME_LENGTH chars
    chars_before: int  # total de chars lidos (antes da truncagem)
    chars_after: int   # chars efetivamente armazenados


def truncate(raw: str) -> TruncatedLexeme:
    upper = raw.upper()
    stored = upper[:MAX_LEXEME_LENGTH]
    return TruncatedLexeme(
        stored=stored,
        chars_before=len(upper),
        chars_after=len(stored),
    )
