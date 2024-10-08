from typing import List, Optional


class ConceptsProduct:
    def __init__(
        self, concepts: List[str], is_valid: bool, error: Optional[str] = None
    ):
        self._concepts = concepts
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._concepts

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
