from typing import List


class TextsProduct:

    def __init__(self, texts: List[str], is_valid: bool, error: str = None):
        self._texts = texts
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[str]:
        return self._texts

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
