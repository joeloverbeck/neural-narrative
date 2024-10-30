from typing import Optional

from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager


class CharacterInformationProvider:

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_memories: Optional[CharacterMemories] = None,
            path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier

        self._character_memories = character_memories or CharacterMemories(
            self._playthrough_name
        )
        self._path_manager = path_manager or PathManager()

    def get_information(self) -> str:
        character_information = read_file(
            self._path_manager.get_character_information_path()
        )
        character = Character(self._playthrough_name, self._character_identifier)
        memories = self._character_memories.load_memories(character)
        character_information = character_information.format(
            **{
                "name": character.name,
                "description": character.description,
                "personality": character.personality,
                "profile": character.profile,
                "likes": character.likes,
                "dislikes": character.dislikes,
                "secrets": character.secrets,
                "speech_patterns": character.speech_patterns,
                "health": character.health,
                "equipment": character.equipment,
                "memories": memories,
            }
        )
        return character_information
