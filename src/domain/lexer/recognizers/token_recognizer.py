from abc import ABC, abstractmethod
from ...protocols.char_stream import CharStream
from ...token.token import Token


class TokenRecognizer(ABC):
    """Strategy ABC — cada subclasse implementa um reconhecedor de átomo."""

    @abstractmethod
    def can_handle(self, ch: str) -> bool:
        """Retorna True se este reconhecedor trata o caractere inicial ch."""
        ...

    @abstractmethod
    def recognize(self, stream: CharStream) -> Token:
        """Lê do stream e retorna o Token reconhecido."""
        ...
