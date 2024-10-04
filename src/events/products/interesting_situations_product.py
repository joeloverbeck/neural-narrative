from typing import List


class InterestingSituationsProduct:

    def __init__(
        self, interesting_situations: List[str], is_valid: bool, error: str = None
    ):
        self._interesting_situations = interesting_situations
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._interesting_situations

    def is_valid(self) -> bool:
        return self._is_valid

    def error(self) -> str:
        return self._error
