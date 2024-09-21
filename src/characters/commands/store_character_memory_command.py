import logging

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class StoreCharacterMemoryCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        memory: str,
        filesystem_manager: FilesystemManager = None,
        characters_manager: CharactersManager = None,
    ):
        if not isinstance(character_identifier, str):
            raise TypeError(
                f"character_identifier should be a string, but it was {type(character_identifier)}."
            )

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._memory = memory

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        character_data = self._characters_manager.load_character_data(
            self._character_identifier
        )

        file_path = self._filesystem_manager.get_file_path_to_character_memories(
            self._playthrough_name, self._character_identifier, character_data["name"]
        )

        self._filesystem_manager.write_file(file_path, self._memory + "\n")

        logger.info(f"Saved memory at '{file_path}'.")
