from typing import List

from src.characters.algorithms.join_characters_memories_algorithm import (
    JoinCharactersMemoriesAlgorithm,
)
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)


class JoinCharactersMemoriesAlgorithmFactory:

    def __init__(
        self, retrieve_memories_algorithm_factory: RetrieveMemoriesAlgorithmFactory
    ):
        self._retrieve_memories_algorithm_factory = retrieve_memories_algorithm_factory

    def create_algorithm(
        self, character_identifiers: List[str], query_text: str
    ) -> JoinCharactersMemoriesAlgorithm:
        return JoinCharactersMemoriesAlgorithm(
            character_identifiers,
            query_text,
            self._retrieve_memories_algorithm_factory,
        )
