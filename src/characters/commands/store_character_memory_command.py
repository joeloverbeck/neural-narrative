import logging
from pathlib import Path
from typing import Optional

from src.base.abstracts.command import Command
from src.characters.character import Character
from src.filesystem.file_operations import append_to_file, create_directories
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class StoreCharacterMemoryCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        memory: str,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._memory = memory

        self._path_manager = path_manager or PathManager()

    def execute(self) -> None:
        character = Character(self._playthrough_name, self._character_identifier)

        # Ensure that the character folder exists.
        create_directories(
            self._path_manager.get_character_path(
                self._playthrough_name, character.identifier, character.name
            )
        )

        file_path = self._path_manager.get_memories_path(
            self._playthrough_name, self._character_identifier, character.name
        )

        append_to_file(Path(file_path), "\n" + self._memory.replace("\n\n", " "))

        logger.info(f"Saved memory at '{file_path}'.")
