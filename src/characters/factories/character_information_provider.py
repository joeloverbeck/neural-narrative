from typing import Optional

from src.base.constants import CHARACTER_INFORMATION_BLOCK
from src.base.required_string import RequiredString
from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.filesystem.filesystem_manager import FilesystemManager


class CharacterInformationProvider:
    def __init__(
        self,
            playthrough_name: RequiredString,
            character_identifier: RequiredString,
        filesystem_manager: Optional[FilesystemManager] = None,
        character_memories: Optional[CharacterMemories] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._character_memories = character_memories or CharacterMemories(
            self._playthrough_name
        )

    def get_information(self) -> str:
        # Load the corresponding block
        character_information = self._filesystem_manager.read_file(
            RequiredString(CHARACTER_INFORMATION_BLOCK)
        )

        character = Character(self._playthrough_name, self._character_identifier)

        memories = self._character_memories.load_memories(character)

        character_information = character_information.value.format(
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
