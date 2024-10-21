from typing import List

from src.base.required_string import RequiredString


class InterestingDilemmasProduct:

    def __init__(
            self,
            interesting_dilemmas: List[RequiredString],
            is_valid: bool,
            error: str = None,
    ):
        self._interesting_dilemmas = interesting_dilemmas
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[RequiredString]:
        return self._interesting_dilemmas

    def is_valid(self) -> bool:
        return self._is_valid

    def error(self) -> str:
        return self._error
