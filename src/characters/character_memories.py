from typing import Optional, List

from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.filesystem.file_operations import (
    read_file,
    write_file,
    create_empty_file_if_not_exists,
    create_directories,
)
from src.filesystem.path_manager import PathManager


class CharacterMemories:

    def __init__(
        self,
        playthrough_name: str,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()

    def load_memories(self, character: Character) -> Optional[str]:
        # Ensure that the character folder exists.
        create_directories(
            self._path_manager.get_character_path(
                self._playthrough_name, character.identifier, character.name
            )
        )

        file_path = self._path_manager.get_memories_path(
            self._playthrough_name, character.identifier, character.name
        )

        create_empty_file_if_not_exists(file_path)

        return read_file(file_path)

    def save_memories(self, character: Character, memories: str):
        file_path = self._path_manager.get_memories_path(
            self._playthrough_name, character.identifier, character.name
        )

        write_file(file_path, memories)

    def join_characters_memories(self, characters: List[Character]) -> List[str]:
        joined_memories = []
        for character in characters:
            memories = self.load_memories(character)
            memories_list = [
                memory.strip()
                for memory in memories.strip().split("\n")
                if memory.strip()
            ]
            joined_memories.extend(memories_list)
        return joined_memories
