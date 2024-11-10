from typing import Optional

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    read_file,
    create_empty_file_if_not_exists,
    write_file,
)
from src.filesystem.path_manager import PathManager


class FactsRepository:

    def __init__(
        self, playthrough_name: str, path_manager: Optional[PathManager] = None
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._path_manager = path_manager or PathManager()

        self._facts_path = self._path_manager.get_facts_path(self._playthrough_name)

    def load_facts_file(self) -> str:
        create_empty_file_if_not_exists(self._facts_path)

        return read_file(self._facts_path)

    def save_facts(self, facts: str):
        # This overwrites the previous facts.
        write_file(self._facts_path, facts)
