from pathlib import Path
from typing import Optional

from src.characters.character import Character
from src.filesystem.file_operations import read_file, write_file
from src.filesystem.filesystem_manager import FilesystemManager


class CharacterMemories:

    def __init__(
        self,
        playthrough_name: str,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def load_memories(self, character: Character) -> Optional[str]:
        file_path = self._filesystem_manager.get_file_path_to_character_memories(
            self._playthrough_name, character.identifier, character.name
        )

        self._filesystem_manager.create_empty_file_if_not_exists(file_path)

        return read_file(Path(file_path))

    def save_memories(self, character: Character, memories: str):
        file_path = self._filesystem_manager.get_file_path_to_character_memories(
            self._playthrough_name, character.identifier, character.name
        )

        write_file(Path(file_path), memories)
