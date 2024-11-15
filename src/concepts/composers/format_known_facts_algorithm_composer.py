from src.base.validators import validate_non_empty_string
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.databases.chroma_db_database import ChromaDbDatabase
from src.filesystem.config_loader import ConfigLoader


class FormatKnownFactsAlgorithmComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_algorithm(self) -> FormatKnownFactsAlgorithm:
        database = ChromaDbDatabase(self._playthrough_name)

        config_loader = ConfigLoader()

        return FormatKnownFactsAlgorithm(database, config_loader)
