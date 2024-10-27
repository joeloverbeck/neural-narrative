from typing import List


class CombineMemoriesAlgorithm:
    def __init__(self, memories_1: List[str], memories_2: List[str]):
        self._memories_1 = memories_1
        self._memories_2 = memories_2

    def do_algorithm(self) -> List[str]:
        all_memories = self._memories_1.copy()
        all_memories.extend(self._memories_2)
        seen = set()
        unique_memories = []
        for memory in all_memories:
            if memory not in seen:
                seen.add(memory)
                unique_memories.append(memory)
        return unique_memories
