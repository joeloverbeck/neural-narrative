from typing import List, Optional


class GoalsProduct:

    def __init__(self, goals: List[str], is_valid: bool, error: Optional[str] = None):
        self._goals = goals
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._goals

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
