from typing import List, Optional

from src.base.required_string import RequiredString


class GoalsProduct:
    def __init__(
            self, goals: List[RequiredString], is_valid: bool, error: Optional[str] = None
    ):
        self._goals = goals
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[RequiredString]:
        return self._goals

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
