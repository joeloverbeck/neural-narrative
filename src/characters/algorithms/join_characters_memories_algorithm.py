from typing import List

from src.base.validators import validate_non_empty_string
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)


class JoinCharactersMemoriesAlgorithm:
    def __init__(
        self,
        character_identifiers: List[str],
        query_text: str,
        retrieve_memories_algorithm_factories: RetrieveMemoriesAlgorithmFactory,
    ):
        validate_non_empty_string(query_text, "query_text")

        self._character_identifiers = character_identifiers
        self._query_text = query_text
        self._retrieve_memories_algorithm_factories = (
            retrieve_memories_algorithm_factories
        )

    def do_algorithm(self) -> List[str]:
        processed_identifiers = []
        joined_memories = []

        for character_identifier in self._character_identifiers:
            if character_identifier not in processed_identifiers:
                processed_identifiers.append(character_identifier)
            else:
                continue

            joined_memories.extend(
                self._retrieve_memories_algorithm_factories.create_algorithm(
                    character_identifier, self._query_text
                ).do_algorithm()
            )

        return joined_memories
