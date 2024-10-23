from typing import List


class ScenariosProduct:

    def __init__(self, scenarios: List[str], is_valid: bool, error: str = None):
        self._scenarios = scenarios
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._scenarios

    def is_valid(self) -> bool:
        return self._is_valid

    def error(self) -> str:
        return self._error
