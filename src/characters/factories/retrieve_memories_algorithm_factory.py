from src.characters.algorithms.retrieve_memories_algorithm import (
    RetrieveMemoriesAlgorithm,
)
from src.databases.abstracts.database import Database


class RetrieveMemoriesAlgorithmFactory:
    def __init__(self, database: Database):
        self._database = database

    def create_algorithm(
        self,
        character_identifier: str,
        query_text: str,
    ) -> RetrieveMemoriesAlgorithm:
        return RetrieveMemoriesAlgorithm(
            character_identifier, query_text, self._database
        )
