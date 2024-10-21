from typing import List

from src.base.required_string import RequiredString


class CharacterGenerationGuidelinesProduct:
    def __init__(
            self, guidelines: List[RequiredString], is_valid: bool, error: str = None
    ):
        self._guidelines = guidelines
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[RequiredString]:
        return self._guidelines

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
