from typing import List


class DilemmasProduct:

    def __init__(self, dilemmas: List[str], is_valid: bool, error: str = None):
        self._dilemmas = dilemmas
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._dilemmas

    def is_valid(self) -> bool:
        return self._is_valid

    def error(self) -> str:
        return self._error
