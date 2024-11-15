from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager


class CharacterInformationProvider:

    def __init__(
        self,
        character_identifier: str,
        query_text: str,
        retrieve_memories_algorithm_factory: RetrieveMemoriesAlgorithmFactory,
        character_factory: CharacterFactory,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(query_text, "query_text")

        self._character_identifier = character_identifier
        self._query_text = query_text
        self._retrieve_memories_algorithm_factory = retrieve_memories_algorithm_factory
        self._character_factory = character_factory

        self._path_manager = path_manager or PathManager()

    def get_information(self) -> str:
        character_information = read_file(
            self._path_manager.get_character_information_path()
        )

        character = self._character_factory.create_character(self._character_identifier)

        memories = "\n".join(
            self._retrieve_memories_algorithm_factory.create_algorithm(
                character.identifier, self._query_text
            ).do_algorithm()
        )

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
