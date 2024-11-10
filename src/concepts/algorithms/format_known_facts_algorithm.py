from typing import Optional

from src.concepts.repositories.facts_repository import FactsRepository


class FormatKnownFactsAlgorithm:
    def __init__(
        self, playthrough_name: str, facts_repository: Optional[FactsRepository] = None
    ):

        self._facts_repository = facts_repository or FactsRepository(playthrough_name)

    def do_algorithm(self) -> str:
        facts_file = self._facts_repository.load_facts_file()

        known_facts = ""
        if facts_file:
            known_facts = "Known Facts:\n" + facts_file

        return known_facts
