from typing import List

from src.characters.algorithms.combine_memories_algorithm import (
    CombineMemoriesAlgorithm,
)


class CombineMemoriesAlgorithmFactory:

    @staticmethod
    def create_algorithm(memories_1: List[str], memories_2: List[str]):
        return CombineMemoriesAlgorithm(memories_1, memories_2)
