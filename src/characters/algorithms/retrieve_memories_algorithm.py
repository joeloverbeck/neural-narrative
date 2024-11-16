from typing import Optional, List

from src.base.validators import validate_non_empty_string
from src.databases.abstracts.database import Database
from src.filesystem.config_loader import ConfigLoader


class RetrieveMemoriesAlgorithm:

    def __init__(
        self,
        character_identifier: str,
        query_text: str,
        database: Database,
        config_loader: Optional[ConfigLoader] = None,
    ):
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(query_text, "query_text")

        self._character_identifier = character_identifier
        self._query_text = query_text
        self._database = database

        self._config_loader = config_loader or ConfigLoader()

    def do_algorithm(self) -> List[str]:
        results = self._database.retrieve_memories(
            self._character_identifier,
            self._query_text,
            self._config_loader.get_memories_to_retrieve_from_database(),
        )

        return [entry["document"] for entry in results]
