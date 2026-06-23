class LexException(Exception):
    pass


class SourceFileNotFoundException(LexException):
    def __init__(self, path: str) -> None:
        super().__init__(f"Arquivo não encontrado: {path}")


class UnterminatedCommentException(LexException):
    def __init__(self, line: int) -> None:
        super().__init__(f"Comentário de bloco não fechado (aberto na linha {line})")


class UnterminatedStringException(LexException):
    def __init__(self, line: int) -> None:
        super().__init__(f"String não fechada (aberta na linha {line})")
