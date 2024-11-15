from typing import Protocol, List


class Database(Protocol):
    def insert_fact(self, fact: str) -> None:
        pass

    def insert_memory(self, character_identifier: str, memory: str) -> None:
        pass

    def retrieve_facts(self, query_text: str, top_k: int = 5) -> List[str]:
        pass

    def retrieve_memories(
        self, character_identifier: str, query_text: str, top_k: int = 5
    ) -> List[str]:
        pass
