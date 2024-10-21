import logging

from src.base.abstracts.command import Command
from src.base.required_string import RequiredString
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class StoreCharacterMemoryCommand(Command):
    def __init__(
        self,
        playthrough_name: RequiredString,
        character_identifier: RequiredString,
        memory: RequiredString,
        filesystem_manager: FilesystemManager = None,
        characters_manager: CharactersManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._memory = memory

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        character = Character(self._playthrough_name, self._character_identifier)

        file_path = self._filesystem_manager.get_file_path_to_character_memories(
            self._playthrough_name, self._character_identifier, character.name
        )

        self._filesystem_manager.append_to_file(
            file_path, RequiredString("\n" + self._memory.value.replace("\n\n", " "))
        )

        logger.info(f"Saved memory at '{file_path}'.")
