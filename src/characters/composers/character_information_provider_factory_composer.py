from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.databases.chroma_db_database import ChromaDbDatabase


class CharacterInformationProviderFactoryComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_factory(
        self, character_identifier: str
    ) -> CharacterInformationProviderFactory:
        validate_non_empty_string(character_identifier, "character_identifier")

        database = ChromaDbDatabase(self._playthrough_name)

        retrieve_memories_algorithm_factory = RetrieveMemoriesAlgorithmFactory(database)

        character_factory = CharacterFactory(self._playthrough_name)

        return CharacterInformationProviderFactory(
            character_identifier,
            retrieve_memories_algorithm_factory,
            character_factory,
        )
