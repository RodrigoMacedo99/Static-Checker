class ScopeManager:
    """Application Service — rastreia o escopo léxico durante a análise."""

    def __init__(self) -> None:
        self._stack: list[str] = []

    def enter_scope(self, name: str) -> None:
        self._stack.append(name)

    def exit_scope(self) -> None:
        if self._stack:
            self._stack.pop()

    def current(self) -> str:
        return self._stack[-1] if self._stack else "global"

    def depth(self) -> int:
        return len(self._stack)
