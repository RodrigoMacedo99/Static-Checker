from pathlib import Path
from .double_buffer import DoubleBuffer
from ...shared.constants import SOURCE_EXTENSION
from ...shared.exceptions import SourceFileNotFoundException


class FileReader:
    """Abre o arquivo .261 e retorna um DoubleBuffer."""

    def open(self, base_name: str) -> DoubleBuffer:
        path = Path(base_name).with_suffix(SOURCE_EXTENSION)
        if not path.exists():
            raise SourceFileNotFoundException(str(path))
        return DoubleBuffer.from_path(path)
