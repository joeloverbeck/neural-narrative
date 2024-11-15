from typing import Optional

from src.databases.abstracts.database import Database
from src.filesystem.config_loader import ConfigLoader


class FormatKnownFactsAlgorithm:
    def __init__(
        self, database: Database, config_loader: Optional[ConfigLoader] = None
    ):
        if isinstance(database, str):
            raise TypeError(
                "The database should have been compatible with the Protocol Database, but was a string."
            )

        self._database = database

        self._config_loader = config_loader or ConfigLoader()

    def do_algorithm(self, query_text: str) -> str:
        facts = self._database.retrieve_facts(
            query_text, self._config_loader.get_facts_to_retrieve_from_database()
        )

        known_facts = ""

        if facts:
            known_facts = "Known Facts:\n" + "\n".join(facts)

        return known_facts
