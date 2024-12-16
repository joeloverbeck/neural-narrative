from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.characters.providers.character_information_provider import (
    CharacterInformationProvider,
)


class CharacterInformationProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        retrieve_memories_algorithm_factory: RetrieveMemoriesAlgorithmFactory,
        character_factory: CharacterFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._retrieve_memories_algorithm_factory = retrieve_memories_algorithm_factory
        self._character_factory = character_factory

    def create_provider(
        self, query_text: str, use_interview: bool = False, use_memories: bool = True
    ):
        return CharacterInformationProvider(
            self._playthrough_name,
            self._character_identifier,
            query_text,
            self._retrieve_memories_algorithm_factory,
            use_interview,
            use_memories,
            self._character_factory,
        )
